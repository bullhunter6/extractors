"""WebSocket endpoint for real-time updates."""
import asyncio
import json
from datetime import datetime
from typing import Set, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.core.database import get_db
from server.models import Extractor, ExtractorStatus
from server.schemas import WSMessage, ExtractorStatusUpdate
from server.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/ws", tags=["websocket"])


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info("WebSocket connected", total_connections=len(self.active_connections))
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info("WebSocket disconnected", total_connections=len(self.active_connections))
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error("Failed to send message", error=str(e))
                disconnected.add(connection)
        
        # Clean up disconnected clients
        self.active_connections -= disconnected
    
    async def send_personal(self, message: dict, websocket: WebSocket):
        """Send message to specific client."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error("Failed to send personal message", error=str(e))


manager = ConnectionManager()


@router.websocket("/status")
async def websocket_status_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time extractor status updates.
    
    Sends updates when:
    - Extractor status changes
    - New task starts
    - Task completes
    - Extractor is enabled/disabled
    """
    await manager.connect(websocket)
    
    try:
        # Send initial status on connection
        from server.core.database import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Extractor))
            extractors = result.scalars().all()
            
            initial_status = WSMessage(
                type="initial_status",
                data={
                    "extractors": [
                        {
                            "id": e.id,
                            "name": e.name,
                            "status": e.status.value,
                            "enabled": e.enabled,
                            "current_task_id": e.current_task_id
                        }
                        for e in extractors
                    ]
                }
            )
            await manager.send_personal(initial_status.model_dump(), websocket)
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for messages from client (ping/pong, etc.)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                
                # Handle client messages if needed
                try:
                    client_msg = json.loads(data)
                    if client_msg.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                except json.JSONDecodeError:
                    pass
                    
            except asyncio.TimeoutError:
                # Send periodic heartbeat
                await websocket.send_json({"type": "heartbeat", "timestamp": datetime.utcnow().isoformat()})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected normally")
    except Exception as e:
        manager.disconnect(websocket)
        logger.error("WebSocket error", error=str(e))


async def broadcast_status_update(
    extractor_id: int,
    extractor_name: str,
    status: ExtractorStatus,
    task_id: str = None
):
    """
    Broadcast extractor status update to all connected clients.
    
    This should be called from API endpoints when status changes.
    """
    update = ExtractorStatusUpdate(
        extractor_id=extractor_id,
        extractor_name=extractor_name,
        status=status,
        task_id=task_id
    )
    
    message = WSMessage(
        type="status_update",
        data=update.model_dump()
    )
    
    await manager.broadcast(message.model_dump())


class LogConnectionManager:
    """Manage WebSocket connections for log streaming."""
    
    def __init__(self):
        # Maps extractor_id -> set of websocket connections
        self.connections: Dict[int, Set[WebSocket]] = {}
        self.all_logs_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket, extractor_id: int = None):
        """Accept new WebSocket connection for logs."""
        await websocket.accept()
        
        if extractor_id:
            if extractor_id not in self.connections:
                self.connections[extractor_id] = set()
            self.connections[extractor_id].add(websocket)
            logger.info("Log WebSocket connected", extractor_id=extractor_id)
        else:
            self.all_logs_connections.add(websocket)
            logger.info("Global log WebSocket connected")
    
    def disconnect(self, websocket: WebSocket, extractor_id: int = None):
        """Remove WebSocket connection."""
        if extractor_id and extractor_id in self.connections:
            self.connections[extractor_id].discard(websocket)
        self.all_logs_connections.discard(websocket)
    
    async def send_log(self, extractor_id: int, log_entry: dict):
        """Send log to subscribers of specific extractor."""
        disconnected = set()
        
        # Send to extractor-specific subscribers
        if extractor_id in self.connections:
            for ws in self.connections[extractor_id]:
                try:
                    await ws.send_json(log_entry)
                except Exception:
                    disconnected.add(ws)
            self.connections[extractor_id] -= disconnected
        
        # Send to global subscribers
        disconnected = set()
        for ws in self.all_logs_connections:
            try:
                await ws.send_json(log_entry)
            except Exception:
                disconnected.add(ws)
        self.all_logs_connections -= disconnected


log_manager = LogConnectionManager()


@router.websocket("/logs/{extractor_id}")
async def websocket_logs_endpoint(websocket: WebSocket, extractor_id: int):
    """
    WebSocket endpoint for real-time log streaming for a specific extractor.
    """
    await log_manager.connect(websocket, extractor_id)
    
    try:
        # Subscribe to Redis channel for this extractor's logs
        import redis.asyncio as aioredis
        from server.core.config import get_settings
        
        settings = get_settings()
        redis_client = aioredis.from_url(settings.REDIS_URL)
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"extractor:{extractor_id}:logs")
        
        async def listen_redis():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        log_data = json.loads(message["data"])
                        await websocket.send_json(log_data)
                    except Exception:
                        pass
        
        async def listen_websocket():
            while True:
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                    if data == "ping":
                        await websocket.send_json({"type": "pong"})
                except asyncio.TimeoutError:
                    await websocket.send_json({"type": "heartbeat"})
        
        # Run both listeners concurrently
        await asyncio.gather(listen_redis(), listen_websocket())
        
    except WebSocketDisconnect:
        log_manager.disconnect(websocket, extractor_id)
    except Exception as e:
        log_manager.disconnect(websocket, extractor_id)
        logger.error("Log WebSocket error", error=str(e))
    finally:
        await pubsub.unsubscribe(f"extractor:{extractor_id}:logs")
        await redis_client.close()


@router.websocket("/logs")
async def websocket_all_logs_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time log streaming for all extractors.
    """
    await log_manager.connect(websocket)
    
    try:
        import redis.asyncio as aioredis
        from server.core.config import get_settings
        
        settings = get_settings()
        redis_client = aioredis.from_url(settings.REDIS_URL)
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("extractors:logs")
        
        async def listen_redis():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        log_data = json.loads(message["data"])
                        await websocket.send_json(log_data)
                    except Exception:
                        pass
        
        async def listen_websocket():
            while True:
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                    if data == "ping":
                        await websocket.send_json({"type": "pong"})
                except asyncio.TimeoutError:
                    await websocket.send_json({"type": "heartbeat"})
        
        await asyncio.gather(listen_redis(), listen_websocket())
        
    except WebSocketDisconnect:
        log_manager.disconnect(websocket)
    except Exception as e:
        log_manager.disconnect(websocket)
        logger.error("Global log WebSocket error", error=str(e))
    finally:
        await pubsub.unsubscribe("extractors:logs")
        await redis_client.close()

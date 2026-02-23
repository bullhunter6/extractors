"""Real-time log streaming via Redis pub/sub."""
import json
import logging
from datetime import datetime
from typing import Optional
import redis.asyncio as redis

from server.core.config import get_settings

settings = get_settings()

# Redis client for pub/sub
_redis_client: Optional[redis.Redis] = None


class RedisLogHandler(logging.Handler):
    """
    Custom logging handler that publishes log messages to Redis for real-time streaming.
    This captures logs from extractors that use the standard logging module.
    """
    
    def __init__(self, extractor_id: int, task_id: str, extractor_name: str):
        super().__init__()
        self.extractor_id = extractor_id
        self.task_id = task_id
        self.extractor_name = extractor_name
        self._redis_client = None
        self.logs: list[dict] = []
        self.setLevel(logging.DEBUG)
    
    def _get_client(self):
        if self._redis_client is None:
            import redis as sync_redis
            self._redis_client = sync_redis.from_url(settings.REDIS_URL)
        return self._redis_client
    
    def emit(self, record: logging.LogRecord):
        try:
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "message": self.format(record),
                "logger": record.name,
            }
            self.logs.append(entry)
            
            # Publish to Redis
            try:
                client = self._get_client()
                log_data = {
                    "extractor_id": self.extractor_id,
                    "task_id": self.task_id,
                    "extractor_name": self.extractor_name,
                    **entry
                }
                channel = f"extractor:{self.extractor_id}:logs"
                client.publish(channel, json.dumps(log_data))
                client.publish("extractors:logs", json.dumps(log_data))
            except Exception:
                pass  # Don't fail if Redis is unavailable
        except Exception:
            pass  # Don't break logging
    
    def get_logs_text(self) -> str:
        """Get all captured logs as formatted text."""
        lines = []
        for log in self.logs:
            ts = log.get("timestamp", "")
            level = log.get("level", "INFO")
            msg = log.get("message", "")
            lines.append(f"[{ts}] [{level}] {msg}")
        return "\n".join(lines)


async def get_redis_client() -> redis.Redis:
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_URL)
    return _redis_client


async def publish_log(
    extractor_id: int,
    task_id: str,
    level: str,
    message: str,
    extra: Optional[dict] = None
) -> None:
    """Publish a log message to Redis channel."""
    client = await get_redis_client()
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "extractor_id": extractor_id,
        "task_id": task_id,
        "level": level,
        "message": message,
        "extra": extra or {}
    }
    
    # Publish to extractor-specific channel
    channel = f"extractor:{extractor_id}:logs"
    await client.publish(channel, json.dumps(log_entry))
    
    # Also publish to global channel for dashboard
    await client.publish("extractors:logs", json.dumps(log_entry))


async def subscribe_to_extractor_logs(extractor_id: int):
    """Subscribe to logs for a specific extractor."""
    client = await get_redis_client()
    pubsub = client.pubsub()
    await pubsub.subscribe(f"extractor:{extractor_id}:logs")
    return pubsub


async def subscribe_to_all_logs():
    """Subscribe to all extractor logs."""
    client = await get_redis_client()
    pubsub = client.pubsub()
    await pubsub.subscribe("extractors:logs")
    return pubsub


class ExtractorLogger:
    """Logger that streams logs to Redis and collects them for database storage."""
    
    def __init__(self, extractor_id: int, task_id: str, extractor_name: str):
        self.extractor_id = extractor_id
        self.task_id = task_id
        self.extractor_name = extractor_name
        self.logs: list[dict] = []
        self._redis_client: Optional[redis.Redis] = None
    
    async def _get_client(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = redis.from_url(settings.REDIS_URL)
        return self._redis_client
    
    def _create_entry(self, level: str, message: str, **kwargs) -> dict:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        self.logs.append(entry)
        return entry
    
    async def _publish(self, entry: dict) -> None:
        try:
            client = await self._get_client()
            log_data = {
                "extractor_id": self.extractor_id,
                "task_id": self.task_id,
                "extractor_name": self.extractor_name,
                **entry
            }
            channel = f"extractor:{self.extractor_id}:logs"
            await client.publish(channel, json.dumps(log_data))
            await client.publish("extractors:logs", json.dumps(log_data))
        except Exception:
            pass  # Don't fail if Redis is unavailable
    
    async def info(self, message: str, **kwargs) -> None:
        entry = self._create_entry("INFO", message, **kwargs)
        await self._publish(entry)
    
    async def warning(self, message: str, **kwargs) -> None:
        entry = self._create_entry("WARNING", message, **kwargs)
        await self._publish(entry)
    
    async def error(self, message: str, **kwargs) -> None:
        entry = self._create_entry("ERROR", message, **kwargs)
        await self._publish(entry)
    
    async def debug(self, message: str, **kwargs) -> None:
        entry = self._create_entry("DEBUG", message, **kwargs)
        await self._publish(entry)
    
    def get_logs_text(self) -> str:
        """Get all logs as formatted text."""
        lines = []
        for log in self.logs:
            ts = log["timestamp"]
            level = log["level"]
            msg = log["message"]
            extra = {k: v for k, v in log.items() if k not in ["timestamp", "level", "message"]}
            extra_str = " ".join(f"{k}={v}" for k, v in extra.items()) if extra else ""
            lines.append(f"[{ts}] [{level}] {msg} {extra_str}".strip())
        return "\n".join(lines)


# Synchronous wrapper for use in Celery tasks
class SyncExtractorLogger:
    """Synchronous logger for Celery tasks."""
    
    def __init__(self, extractor_id: int, task_id: str, extractor_name: str):
        self.extractor_id = extractor_id
        self.task_id = task_id
        self.extractor_name = extractor_name
        self.logs: list[dict] = []
        self._redis_client = None
    
    def _get_client(self):
        if self._redis_client is None:
            import redis as sync_redis
            self._redis_client = sync_redis.from_url(settings.REDIS_URL)
        return self._redis_client
    
    def _create_entry(self, level: str, message: str, **kwargs) -> dict:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        self.logs.append(entry)
        return entry
    
    def _publish(self, entry: dict) -> None:
        try:
            client = self._get_client()
            log_data = {
                "extractor_id": self.extractor_id,
                "task_id": self.task_id,
                "extractor_name": self.extractor_name,
                **entry
            }
            channel = f"extractor:{self.extractor_id}:logs"
            client.publish(channel, json.dumps(log_data))
            client.publish("extractors:logs", json.dumps(log_data))
        except Exception:
            pass  # Don't fail if Redis is unavailable
    
    def info(self, message: str, **kwargs) -> None:
        entry = self._create_entry("INFO", message, **kwargs)
        self._publish(entry)
    
    def warning(self, message: str, **kwargs) -> None:
        entry = self._create_entry("WARNING", message, **kwargs)
        self._publish(entry)
    
    def error(self, message: str, **kwargs) -> None:
        entry = self._create_entry("ERROR", message, **kwargs)
        self._publish(entry)
    
    def debug(self, message: str, **kwargs) -> None:
        entry = self._create_entry("DEBUG", message, **kwargs)
        self._publish(entry)
    
    def get_logs_text(self) -> str:
        """Get all logs as formatted text."""
        lines = []
        for log in self.logs:
            ts = log["timestamp"]
            level = log["level"]
            msg = log["message"]
            extra = {k: v for k, v in log.items() if k not in ["timestamp", "level", "message"]}
            extra_str = " ".join(f"{k}={v}" for k, v in extra.items()) if extra else ""
            lines.append(f"[{ts}] [{level}] {msg} {extra_str}".strip())
        return "\n".join(lines)

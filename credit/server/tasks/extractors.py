"""Celery tasks for running extractors."""
import logging
import time
import traceback
from datetime import datetime
from typing import Any, Callable

from celery import Task
from sqlalchemy import update
from server.core.celery_app import celery_app
from server.core.logging import get_logger
from server.core.database import get_sync_db
from server.core.log_stream import SyncExtractorLogger, RedisLogHandler
from server.models import Extractor, ExtractorRun, ExtractorStatus

logger = get_logger(__name__)


class ExtractorTask(Task):
    """Base task class for extractors with error handling."""
    
    def on_failure(self, exc: Exception, task_id: str, args: tuple, kwargs: dict, einfo: Any) -> None:
        """Handle task failure."""
        logger.error(
            "Task failed",
            task_id=task_id,
            error=str(exc),
            traceback=str(einfo)
        )
    
    def on_success(self, retval: Any, task_id: str, args: tuple, kwargs: dict) -> None:
        """Handle task success."""
        logger.info(
            "Task completed successfully",
            task_id=task_id,
            items_extracted=retval.get("items_extracted", 0) if isinstance(retval, dict) else 0
        )
    
    def on_retry(self, exc: Exception, task_id: str, args: tuple, kwargs: dict, einfo: Any) -> None:
        """Handle task retry."""
        logger.warning(
            "Task retrying",
            task_id=task_id,
            error=str(exc),
            retry_count=self.request.retries
        )


@celery_app.task(
    base=ExtractorTask,
    bind=True,
    name="server.tasks.extractors.run_extractor",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def run_extractor(
    self: Task,
    extractor_id: int,
    module_path: str,
    function_name: str,
    extractor_name: str
) -> dict:
    """
    Run an extractor function as a Celery task.
    """
    import sys
    from pathlib import Path
    
    # Add project root to path for extractor imports
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    start_time = time.time()
    task_id = self.request.id

    # Check if a global stop has been requested (set by stop-all endpoint)
    try:
        import redis as redis_lib
        from server.core.config import get_settings
        _settings = get_settings()
        _r = redis_lib.from_url(_settings.CELERY_BROKER_URL)
        if _r.get("extractors:stop_all_requested"):
            logger.warning(f"Stop-all flag set — aborting task {task_id} for {extractor_name}")
            # Reset this extractor to IDLE since we're not running it
            try:
                from sqlalchemy import update as _upd
                from server.core.database import get_sync_db
                with get_sync_db() as _sess:
                    _sess.execute(
                        _upd(Extractor).where(Extractor.id == extractor_id)
                        .values(status=ExtractorStatus.IDLE, current_task_id=None)
                    )
                    _sess.commit()
            except Exception:
                pass
            return {"status": "aborted", "reason": "stop_all_requested", "extractor_id": extractor_id}
    except Exception:
        pass  # If Redis check fails, proceed normally

    # Create logger for real-time streaming
    ext_logger = SyncExtractorLogger(extractor_id, task_id, extractor_name)
    
    # Create a logging handler to capture extractor's logging output
    # This intercepts logging.info(), logging.error() etc from extractors
    redis_handler = RedisLogHandler(extractor_id, task_id, extractor_name)
    redis_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Add handler to root logger to capture all logging from extractors
    root_logger = logging.getLogger()
    original_level = root_logger.level
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(redis_handler)
    
    ext_logger.info(f"Starting extractor: {extractor_name}")
    ext_logger.info(f"Module: {module_path}, Function: {function_name}")
    ext_logger.info(f"Task ID: {task_id}")
    
    try:
        # Dynamically import the extractor function
        ext_logger.info("Importing module...")
        import importlib
        module = importlib.import_module(module_path)
        extractor_func: Callable = getattr(module, function_name)
        ext_logger.info("Module imported successfully")
        
        # Execute the extractor
        ext_logger.info("Executing extractor function...")
        result = extractor_func()
        
        # Calculate items extracted
        items_extracted = 0
        if isinstance(result, list):
            items_extracted = len(result)
        elif isinstance(result, dict) and "count" in result:
            items_extracted = result["count"]
        
        duration = time.time() - start_time
        
        ext_logger.info(f"Extraction completed successfully!")
        ext_logger.info(f"Items extracted: {items_extracted}")
        ext_logger.info(f"Duration: {round(duration, 2)} seconds")
        
        # Cleanup logging handler
        root_logger.removeHandler(redis_handler)
        root_logger.setLevel(original_level)
        
        # Combine logs from ext_logger and redis_handler (extractor's logging)
        combined_logs = ext_logger.get_logs_text()
        extractor_logs = redis_handler.get_logs_text()
        if extractor_logs:
            combined_logs += "\n" + extractor_logs
        
        # Update database with success
        try:
            _update_extractor_success_sync(
                extractor_id=extractor_id,
                extractor_name=extractor_name,
                task_id=task_id,
                items_extracted=items_extracted,
                duration=round(duration, 2),
                logs=combined_logs
            )
            ext_logger.info("Database updated successfully")
        except Exception as db_error:
            ext_logger.error(f"Failed to update database: {str(db_error)}")
        
        return {
            "status": "success",
            "items_extracted": items_extracted,
            "duration_seconds": round(duration, 2),
            "task_id": task_id,
            "extractor_id": extractor_id
        }
        
    except Exception as exc:
        duration = time.time() - start_time
        error_msg = str(exc)
        error_trace = traceback.format_exc()
        
        ext_logger.error(f"Extractor failed: {error_msg}")
        ext_logger.error(f"Traceback:\n{error_trace}")
        
        # Cleanup logging handler
        root_logger.removeHandler(redis_handler)
        root_logger.setLevel(original_level)
        
        # Combine logs from ext_logger and redis_handler (extractor's logging)
        combined_logs = ext_logger.get_logs_text()
        extractor_logs = redis_handler.get_logs_text()
        if extractor_logs:
            combined_logs += "\n" + extractor_logs
        
        # Update database with failure
        try:
            _update_extractor_failure_sync(
                extractor_id=extractor_id,
                extractor_name=extractor_name,
                task_id=task_id,
                error_msg=error_msg,
                error_trace=error_trace,
                duration=round(duration, 2),
                logs=combined_logs
            )
        except Exception as db_error:
            ext_logger.error(f"Failed to update database: {str(db_error)}")
        
        # Re-raise to trigger Celery retry mechanism
        raise exc


@celery_app.task(name="server.tasks.extractors.run_extractor_batch")
def run_extractor_batch(extractor_configs: list[dict]) -> dict:
    """Run multiple extractors in parallel."""
    from celery import group
    
    logger.info("Starting extractor batch", count=len(extractor_configs))
    
    job = group(
        run_extractor.s(
            extractor_id=config["id"],
            module_path=config["module_path"],
            function_name=config["function_name"],
            extractor_name=config["name"]
        )
        for config in extractor_configs
    )
    
    result = job.apply_async()
    
    return {
        "group_id": result.id,
        "task_count": len(extractor_configs),
        "status": "submitted"
    }


@celery_app.task(name="server.tasks.extractors.health_check")
def health_check() -> dict:
    """Health check task to verify Celery workers are responding."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Database update helpers (sync versions for Celery workers)
def _update_extractor_success_sync(
    extractor_id: int,
    extractor_name: str,
    task_id: str,
    items_extracted: int,
    duration: float,
    logs: str = ""
) -> None:
    """Update database after successful extraction (sync version)."""
    with get_sync_db() as session:
        # Create run record with logs
        run = ExtractorRun(
            extractor_id=extractor_id,
            extractor_name=extractor_name,
            task_id=task_id,
            status="success",
            items_extracted=items_extracted,
            duration_seconds=duration,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            logs=logs
        )
        session.add(run)
        
        # Update extractor status and stats
        stmt = update(Extractor).where(Extractor.id == extractor_id).values(
            status=ExtractorStatus.IDLE,
            current_task_id=None,
            last_run_at=datetime.utcnow(),
            last_success_at=datetime.utcnow(),
            total_runs=Extractor.total_runs + 1,
            successful_runs=Extractor.successful_runs + 1
        )
        session.execute(stmt)
        session.commit()


def _update_extractor_failure_sync(
    extractor_id: int,
    extractor_name: str,
    task_id: str,
    error_msg: str,
    error_trace: str,
    duration: float,
    logs: str = ""
) -> None:
    """Update database after failed extraction (sync version)."""
    with get_sync_db() as session:
        # Create run record with logs
        run = ExtractorRun(
            extractor_id=extractor_id,
            extractor_name=extractor_name,
            task_id=task_id,
            status="failed",
            error_message=error_msg,
            error_traceback=error_trace,
            duration_seconds=duration,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            logs=logs
        )
        session.add(run)
        
        # Update extractor status and stats
        stmt = update(Extractor).where(Extractor.id == extractor_id).values(
            status=ExtractorStatus.ERROR,
            current_task_id=None,
            last_run_at=datetime.utcnow(),
            last_error=error_msg,
            total_runs=Extractor.total_runs + 1,
            failed_runs=Extractor.failed_runs + 1
        )
        session.execute(stmt)
        session.commit()

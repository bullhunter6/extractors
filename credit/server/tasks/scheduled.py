"""Scheduled tasks for automated extractor execution."""
import asyncio
from datetime import datetime, timedelta
from typing import List

from celery import group
from server.core.celery_app import celery_app
from server.core.logging import get_logger
from server.tasks.extractors import run_extractor

logger = get_logger(__name__)


@celery_app.task(name="server.tasks.scheduler.run_scheduled_extractors")
def run_scheduled_extractors():
    """
    Run all enabled extractors that are due for execution.
    
    This task is triggered by Celery Beat and checks which extractors
    should run based on their schedule configuration.
    """
    logger.info("Running scheduled extractors check")

    # Don't queue new tasks if a stop-all was recently requested
    try:
        import redis as redis_lib
        from server.core.config import get_settings
        _r = redis_lib.from_url(get_settings().CELERY_BROKER_URL)
        if _r.get("extractors:stop_all_requested"):
            logger.info("Stop flag active — skipping scheduled run")
            return {"status": "skipped", "reason": "stop_all_requested"}
    except Exception:
        pass

    # Import here to avoid circular dependencies
    from server.core.database import AsyncSessionLocal
    from server.models import Extractor, ExtractorStatus
    from sqlalchemy import select
    
    async def get_due_extractors() -> List[dict]:
        """Get extractors that are due to run and mark them RUNNING atomically."""
        async with AsyncSessionLocal() as db:
            # Get all enabled, non-running extractors
            result = await db.execute(
                select(Extractor).where(
                    (Extractor.enabled == True) &
                    (Extractor.status != ExtractorStatus.RUNNING)
                )
            )
            extractors = result.scalars().all()

            due_extractors = []
            now = datetime.utcnow()

            for extractor in extractors:
                should_run = False

                # Only run if a schedule interval is configured
                if extractor.schedule_interval_minutes:
                    if not extractor.last_run_at:
                        should_run = True
                    else:
                        next_run = extractor.last_run_at + timedelta(
                            minutes=extractor.schedule_interval_minutes
                        )
                        if now >= next_run:
                            should_run = True

                if should_run:
                    # Mark RUNNING immediately so the next tick doesn't re-queue it
                    extractor.status = ExtractorStatus.RUNNING
                    due_extractors.append({
                        'id': extractor.id,
                        'name': extractor.name,
                        'module_path': extractor.module_path,
                        'function_name': extractor.function_name
                    })

            if due_extractors:
                await db.commit()

            return due_extractors

    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    due_extractors = loop.run_until_complete(get_due_extractors())
    loop.close()

    if not due_extractors:
        logger.info("No extractors due to run")
        return {"status": "no_extractors_due", "count": 0}

    logger.info(f"Running {len(due_extractors)} scheduled extractors")

    # Submit each task individually so we can save the task_id back to the DB
    from server.core.database import AsyncSessionLocal
    from server.models import Extractor

    async def save_task_ids(extractor_task_pairs: list):
        async with AsyncSessionLocal() as db:
            for extractor_id, task_id in extractor_task_pairs:
                await db.execute(
                    __import__('sqlalchemy', fromlist=['update']).update(Extractor)
                    .where(Extractor.id == extractor_id)
                    .values(current_task_id=task_id)
                )
            await db.commit()

    pairs = []
    for e in due_extractors:
        task = run_extractor.apply_async(kwargs={
            'extractor_id': e['id'],
            'module_path': e['module_path'],
            'function_name': e['function_name'],
            'extractor_name': e['name']
        })
        pairs.append((e['id'], task.id))

    loop2 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop2)
    loop2.run_until_complete(save_task_ids(pairs))
    loop2.close()

    return {
        "status": "submitted",
        "count": len(due_extractors),
        "task_ids": [p[1] for p in pairs]
    }


@celery_app.task(name="server.tasks.scheduler.cleanup_old_runs")
def cleanup_old_runs(days: int = 30):
    """
    Clean up old extractor run records.
    
    Args:
        days: Delete runs older than this many days (default: 30)
    """
    logger.info(f"Cleaning up runs older than {days} days")
    
    from server.core.database import AsyncSessionLocal
    from server.models import ExtractorRun
    from sqlalchemy import delete
    
    async def cleanup():
        """Perform cleanup."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                delete(ExtractorRun).where(ExtractorRun.started_at < cutoff_date)
            )
            await db.commit()
            return result.rowcount
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    deleted_count = loop.run_until_complete(cleanup())
    loop.close()
    
    logger.info(f"Deleted {deleted_count} old run records")
    
    return {"status": "completed", "deleted_count": deleted_count}


@celery_app.task(name="server.tasks.scheduler.update_system_metrics")
def update_system_metrics():
    """
    Update system-wide metrics snapshot.
    
    Stores current system state for historical tracking.
    """
    from server.core.database import AsyncSessionLocal
    from server.models import Extractor, ExtractorRun, SystemMetrics, ExtractorStatus
    from sqlalchemy import select, func, case, Integer

    async def collect_metrics() -> dict:
        """Collect current system metrics."""
        async with AsyncSessionLocal() as db:
            # Count extractors by status
            extractor_counts = await db.execute(
                select(
                    func.count(Extractor.id).label("total"),
                    func.sum(case((Extractor.enabled == True, 1), else_=0)).label("enabled"),
                    func.sum(case((Extractor.status == ExtractorStatus.RUNNING, 1), else_=0)).label("running")
                )
            )
            counts = extractor_counts.first()
            
            # Count active tasks
            recent_time = datetime.utcnow() - timedelta(minutes=5)
            active_tasks = await db.execute(
                select(func.count()).where(
                    (ExtractorRun.status == ExtractorStatus.RUNNING) &
                    (ExtractorRun.started_at >= recent_time)
                )
            )
            
            # Calculate stats for last 24 hours
            since_24h = datetime.utcnow() - timedelta(hours=24)
            stats = await db.execute(
                select(
                    func.avg(ExtractorRun.duration_seconds).label("avg_duration"),
                    func.count(ExtractorRun.id).label("total"),
                    func.sum(
                        case((ExtractorRun.status == ExtractorStatus.SUCCESS, 1), else_=0)
                    ).label("success")
                ).where(ExtractorRun.completed_at >= since_24h)
            )
            stats_row = stats.first()
            
            success_rate = None
            if stats_row.total and stats_row.total > 0:
                success_rate = (stats_row.success / stats_row.total) * 100
            
            # Create metrics snapshot
            metrics = SystemMetrics(
                timestamp=datetime.utcnow(),
                total_extractors=counts.total or 0,
                enabled_extractors=counts.enabled or 0,
                running_extractors=counts.running or 0,
                active_tasks=active_tasks.scalar() or 0,
                pending_tasks=0,
                avg_duration_seconds=stats_row.avg_duration,
                success_rate=success_rate
            )
            
            db.add(metrics)
            await db.commit()
            
            return {
                "total_extractors": metrics.total_extractors,
                "running_extractors": metrics.running_extractors
            }
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    metrics = loop.run_until_complete(collect_metrics())
    loop.close()
    
    logger.info("System metrics updated", **metrics)
    
    return metrics

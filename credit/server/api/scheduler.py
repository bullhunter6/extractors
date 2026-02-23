"""Scheduler management API endpoints."""
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, desc

from server.core.database import get_db
from server.models import Extractor, ExtractorRun, ExtractorStatus
from server.core.logging import get_logger
from server.tasks.extractors import run_extractor

logger = get_logger(__name__)
router = APIRouter(prefix="/scheduler", tags=["scheduler"])


class ScheduleConfig(BaseModel):
    """Schedule configuration."""
    enabled: bool = True
    interval_minutes: int = Field(60, ge=1, le=1440)  # 1 min to 24 hours


class ScheduleStatus(BaseModel):
    """Current schedule status."""
    enabled: bool
    interval_minutes: int
    next_run_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    last_run_duration_seconds: Optional[float] = None


class SchedulerStats(BaseModel):
    """Comprehensive scheduler statistics."""
    # Overall stats
    total_extractors: int
    enabled_extractors: int
    disabled_extractors: int
    
    # Current status
    running_extractors: int
    idle_extractors: int
    failed_extractors: int
    
    # Run stats (all time)
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    
    # Today's stats
    runs_today: int
    successful_today: int
    failed_today: int
    success_rate_today: float
    
    # Last 24 hours
    runs_last_24h: int
    successful_last_24h: int
    failed_last_24h: int
    avg_duration_last_24h: Optional[float]
    
    # Last scheduled run
    last_scheduled_run_at: Optional[datetime]
    last_scheduled_run_success_count: int
    last_scheduled_run_failure_count: int
    
    # Failed extractors list
    recent_failed_extractors: list[dict]
    
    # Category breakdown
    extractors_by_category: dict[str, int]
    
    # Top performers and worst performers
    top_extractors: list[dict]
    worst_extractors: list[dict]


class BatchTriggerResponse(BaseModel):
    """Response for batch trigger."""
    message: str
    triggered_count: int
    task_ids: list[str]


# In-memory schedule enabled flag (interval is persisted in DB)
_schedule_enabled: bool = True
_last_scheduled_run: Optional[datetime] = None


@router.get("/status", response_model=ScheduleStatus)
async def get_schedule_status(db: AsyncSession = Depends(get_db)) -> ScheduleStatus:
    """Get current schedule status - reads interval from DB so it survives restarts."""
    # Read the interval from the first enabled extractor that has one configured
    result = await db.execute(
        select(Extractor.schedule_interval_minutes)
        .where(
            (Extractor.enabled == True) &
            (Extractor.schedule_interval_minutes != None)
        )
        .limit(1)
    )
    row = result.scalar()
    interval = row if row is not None else 60

    next_run = None
    if _schedule_enabled and _last_scheduled_run:
        next_run = _last_scheduled_run + timedelta(minutes=interval)
    elif _schedule_enabled:
        next_run = datetime.utcnow() + timedelta(minutes=interval)

    return ScheduleStatus(
        enabled=_schedule_enabled,
        interval_minutes=interval,
        next_run_at=next_run,
        last_run_at=_last_scheduled_run
    )


@router.post("/config", response_model=ScheduleStatus)
async def update_schedule_config(config: ScheduleConfig, db: AsyncSession = Depends(get_db)) -> ScheduleStatus:
    """Update schedule configuration."""
    global _schedule_enabled
    _schedule_enabled = config.enabled

    # Propagate interval to all enabled extractors in DB and reset last_run_at so interval starts from now
    from sqlalchemy import update as sa_update
    now = datetime.utcnow()
    await db.execute(
        sa_update(Extractor)
        .where(Extractor.enabled == True)
        .values(schedule_interval_minutes=config.interval_minutes, last_run_at=now)
    )
    await db.commit()

    logger.info(f"Schedule updated: enabled={config.enabled}, interval={config.interval_minutes}min")

    return await get_schedule_status(db)


@router.get("/stats", response_model=SchedulerStats)
async def get_scheduler_stats(db: AsyncSession = Depends(get_db)) -> SchedulerStats:
    """Get comprehensive scheduler statistics."""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_24h = now - timedelta(hours=24)
    
    # Count extractors
    extractor_counts = await db.execute(
        select(
            func.count(Extractor.id).label("total"),
            func.sum(case((Extractor.enabled == True, 1), else_=0)).label("enabled"),
            func.sum(case((Extractor.enabled == False, 1), else_=0)).label("disabled"),
            func.sum(case((Extractor.status == ExtractorStatus.RUNNING, 1), else_=0)).label("running"),
            func.sum(case((Extractor.status == ExtractorStatus.IDLE, 1), else_=0)).label("idle"),
            func.sum(case((Extractor.status == ExtractorStatus.FAILED, 1), else_=0)).label("failed"),
            func.sum(Extractor.total_runs).label("total_runs"),
            func.sum(Extractor.successful_runs).label("successful_runs"),
            func.sum(Extractor.failed_runs).label("failed_runs"),
        )
    )
    counts = extractor_counts.first()
    
    total_runs = counts.total_runs or 0
    successful_runs = counts.successful_runs or 0
    failed_runs = counts.failed_runs or 0
    success_rate = (successful_runs / total_runs * 100) if total_runs > 0 else 0.0
    
    # Today's stats
    today_stats = await db.execute(
        select(
            func.count(ExtractorRun.id).label("runs"),
            func.sum(case((ExtractorRun.status == ExtractorStatus.SUCCESS, 1), else_=0)).label("success"),
            func.sum(case((ExtractorRun.status == ExtractorStatus.FAILED, 1), else_=0)).label("failed"),
        ).where(ExtractorRun.started_at >= today_start)
    )
    today = today_stats.first()
    runs_today = today.runs or 0
    successful_today = today.success or 0
    failed_today = today.failed or 0
    success_rate_today = (successful_today / runs_today * 100) if runs_today > 0 else 0.0
    
    # Last 24 hours stats
    last_24h_stats = await db.execute(
        select(
            func.count(ExtractorRun.id).label("runs"),
            func.sum(case((ExtractorRun.status == ExtractorStatus.SUCCESS, 1), else_=0)).label("success"),
            func.sum(case((ExtractorRun.status == ExtractorStatus.FAILED, 1), else_=0)).label("failed"),
            func.avg(ExtractorRun.duration_seconds).label("avg_duration"),
        ).where(ExtractorRun.started_at >= last_24h)
    )
    last_24h_data = last_24h_stats.first()
    
    # Last batch run info (get the most recent batch by looking for runs started within same minute)
    last_run_result = await db.execute(
        select(ExtractorRun.started_at)
        .order_by(desc(ExtractorRun.started_at))
        .limit(1)
    )
    last_scheduled = last_run_result.scalar()
    
    last_run_success = 0
    last_run_failure = 0
    if last_scheduled:
        # Get stats for that run batch (within 2 minutes of start)
        batch_start = last_scheduled - timedelta(minutes=2)
        batch_stats = await db.execute(
            select(
                func.sum(case((ExtractorRun.status == ExtractorStatus.SUCCESS, 1), else_=0)).label("success"),
                func.sum(case((ExtractorRun.status == ExtractorStatus.FAILED, 1), else_=0)).label("failed"),
            ).where(
                (ExtractorRun.started_at >= batch_start) &
                (ExtractorRun.started_at <= last_scheduled + timedelta(minutes=2))
            )
        )
        batch = batch_stats.first()
        last_run_success = batch.success or 0
        last_run_failure = batch.failed or 0
    
    # Recent failed extractors
    failed_extractors_result = await db.execute(
        select(
            Extractor.id,
            Extractor.name,
            Extractor.last_error,
            Extractor.last_run_at,
            Extractor.failed_runs,
        )
        .where(Extractor.status == ExtractorStatus.FAILED)
        .order_by(desc(Extractor.last_run_at))
        .limit(10)
    )
    recent_failed = [
        {
            "id": row.id,
            "name": row.name,
            "last_error": row.last_error,
            "last_run_at": row.last_run_at.isoformat() if row.last_run_at else None,
            "failed_runs": row.failed_runs,
        }
        for row in failed_extractors_result.all()
    ]
    
    # Category breakdown
    category_result = await db.execute(
        select(
            Extractor.category,
            func.count(Extractor.id).label("count")
        ).group_by(Extractor.category)
    )
    extractors_by_category = {
        str(row.category.value) if row.category else "unknown": row.count
        for row in category_result.all()
    }
    
    # Top performers (highest success rate with at least 5 runs)
    top_result = await db.execute(
        select(
            Extractor.id,
            Extractor.name,
            Extractor.total_runs,
            Extractor.successful_runs,
        )
        .where(Extractor.total_runs >= 5)
        .order_by(desc(Extractor.successful_runs * 1.0 / Extractor.total_runs))
        .limit(5)
    )
    top_extractors = [
        {
            "id": row.id,
            "name": row.name,
            "total_runs": row.total_runs,
            "success_rate": round((row.successful_runs / row.total_runs) * 100, 1) if row.total_runs > 0 else 0,
            "avg_duration": None,
        }
        for row in top_result.all()
    ]
    
    # Worst performers (lowest success rate with at least 5 runs)
    worst_result = await db.execute(
        select(
            Extractor.id,
            Extractor.name,
            Extractor.total_runs,
            Extractor.successful_runs,
            Extractor.failed_runs,
            Extractor.last_error,
        )
        .where(Extractor.total_runs >= 5)
        .order_by(Extractor.successful_runs * 1.0 / Extractor.total_runs)
        .limit(5)
    )
    worst_extractors = [
        {
            "id": row.id,
            "name": row.name,
            "total_runs": row.total_runs,
            "failed_runs": row.failed_runs,
            "success_rate": round((row.successful_runs / row.total_runs) * 100, 1) if row.total_runs > 0 else 0,
            "last_error": row.last_error[:100] if row.last_error else None,
        }
        for row in worst_result.all()
    ]
    
    return SchedulerStats(
        total_extractors=counts.total or 0,
        enabled_extractors=counts.enabled or 0,
        disabled_extractors=counts.disabled or 0,
        running_extractors=counts.running or 0,
        idle_extractors=counts.idle or 0,
        failed_extractors=counts.failed or 0,
        total_runs=total_runs,
        successful_runs=successful_runs,
        failed_runs=failed_runs,
        success_rate=round(success_rate, 2),
        runs_today=runs_today,
        successful_today=successful_today,
        failed_today=failed_today,
        success_rate_today=round(success_rate_today, 2),
        runs_last_24h=last_24h_data.runs or 0,
        successful_last_24h=last_24h_data.success or 0,
        failed_last_24h=last_24h_data.failed or 0,
        avg_duration_last_24h=round(last_24h_data.avg_duration, 2) if last_24h_data.avg_duration else None,
        last_scheduled_run_at=last_scheduled,
        last_scheduled_run_success_count=last_run_success,
        last_scheduled_run_failure_count=last_run_failure,
        recent_failed_extractors=recent_failed,
        extractors_by_category=extractors_by_category,
        top_extractors=top_extractors,
        worst_extractors=worst_extractors,
    )


class StopAllResponse(BaseModel):
    """Response for stop-all."""
    message: str
    revoked_tasks: int
    purged_tasks: int
    reset_extractors: int


@router.post("/stop-all", response_model=StopAllResponse)
async def stop_all_extractors(db: AsyncSession = Depends(get_db)) -> StopAllResponse:
    """
    Stop all running/pending extractor tasks.
    - Sets a Redis stop flag so any queued tasks abort immediately when picked up
    - Revokes active Celery tasks
    - Purges the Celery queue of pending tasks
    - Resets all extractor statuses to IDLE in DB
    """
    from server.core.celery_app import celery_app
    from server.core.config import get_settings
    from sqlalchemy import update as sa_update
    import redis as redis_lib

    settings = get_settings()

    # 1. Set a Redis stop flag briefly so in-flight queued tasks abort on pickup
    r = redis_lib.from_url(settings.CELERY_BROKER_URL)
    r.set("extractors:stop_all_requested", "1", ex=30)  # 30s — just enough for in-flight tasks

    # 2. Collect task IDs of currently running extractors
    running_result = await db.execute(
        select(Extractor.current_task_id).where(
            (Extractor.status == ExtractorStatus.RUNNING) &
            (Extractor.current_task_id != None)
        )
    )
    task_ids = [row[0] for row in running_result.all() if row[0]]

    # 3. Revoke each running task
    for task_id in task_ids:
        celery_app.control.revoke(task_id, terminate=True, signal="SIGTERM")

    # 4. Purge queue directly via Redis (more reliable than control.purge on Windows/solo)
    purged = 0
    try:
        purged = r.llen("celery") or 0
        r.delete("celery")
    except Exception:
        try:
            purged = celery_app.control.purge() or 0
        except Exception:
            pass

    # 5. Reset all running extractors to IDLE in DB and stamp last_run_at=now so interval restarts fresh
    now = datetime.utcnow()
    reset_result = await db.execute(
        sa_update(Extractor)
        .where(Extractor.status.in_([ExtractorStatus.RUNNING, ExtractorStatus.FAILED]))
        .values(status=ExtractorStatus.IDLE, current_task_id=None, last_run_at=now)
        .returning(Extractor.id)
    )
    reset_ids = reset_result.fetchall()
    await db.commit()

    logger.info(
        f"Stop-all: set Redis flag, revoked {len(task_ids)} tasks, purged {purged} queued, "
        f"reset {len(reset_ids)} extractors to IDLE"
    )

    return StopAllResponse(
        message=f"Stopped all extractors: {len(task_ids)} tasks revoked, {purged} purged from queue",
        revoked_tasks=len(task_ids),
        purged_tasks=purged,
        reset_extractors=len(reset_ids),
    )


@router.get("/recent-runs")
async def get_recent_runs(limit: int = 30, db: AsyncSession = Depends(get_db)) -> list:
    """Get the latest N extractor runs across all extractors."""
    result = await db.execute(
        select(ExtractorRun)
        .order_by(desc(ExtractorRun.started_at))
        .limit(limit)
    )
    runs = result.scalars().all()
    return [
        {
            "id": r.id,
            "extractor_name": r.extractor_name,
            "status": r.status.value if hasattr(r.status, 'value') else str(r.status),
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "duration_seconds": round(r.duration_seconds, 1) if r.duration_seconds else None,
            "items_extracted": r.items_extracted,
            "error_message": r.error_message[:120] if r.error_message else None,
        }
        for r in runs
    ]


@router.post("/resume")
async def resume_scheduler() -> dict:
    """Clear the stop flag so the scheduler can run tasks again."""
    from server.core.config import get_settings
    import redis as redis_lib
    settings = get_settings()
    r = redis_lib.from_url(settings.CELERY_BROKER_URL)
    r.delete("extractors:stop_all_requested")
    logger.info("Scheduler resumed — stop flag cleared")
    return {"message": "Scheduler resumed"}


@router.post("/trigger-all", response_model=BatchTriggerResponse)
async def trigger_all_extractors(db: AsyncSession = Depends(get_db)) -> BatchTriggerResponse:
    """Trigger all enabled extractors."""
    global _last_scheduled_run
    
    # Get all enabled extractors
    result = await db.execute(
        select(Extractor)
        .where(Extractor.enabled == True)
        .where(Extractor.status != ExtractorStatus.RUNNING)
    )
    extractors = result.scalars().all()
    
    if not extractors:
        return BatchTriggerResponse(
            message="No extractors available to run",
            triggered_count=0,
            task_ids=[]
        )
    
    task_ids = []
    for extractor in extractors:
        try:
            task = run_extractor.delay(
                extractor_id=extractor.id,
                module_path=extractor.module_path,
                function_name=extractor.function_name,
                extractor_name=extractor.name
            )
            task_ids.append(task.id)
            
            # Update extractor status to running
            extractor.status = ExtractorStatus.RUNNING
            extractor.current_task_id = task.id
        except Exception as e:
            logger.error(f"Failed to trigger extractor {extractor.name}: {e}")
    
    await db.commit()
    _last_scheduled_run = datetime.utcnow()
    
    logger.info(f"Triggered {len(task_ids)} extractors")
    
    return BatchTriggerResponse(
        message=f"Successfully triggered {len(task_ids)} extractors",
        triggered_count=len(task_ids),
        task_ids=task_ids
    )

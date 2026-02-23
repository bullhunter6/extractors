"""Metrics and monitoring API endpoints."""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from server.core.database import get_db
from server.models import Extractor, ExtractorRun, SystemMetrics, ExtractorStatus
from server.schemas import ExtractorMetrics, SystemMetricsResponse
from server.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/extractors", response_model=list[ExtractorMetrics])
async def get_extractor_metrics(
    days: int = Query(7, ge=1, le=90, description="Number of days to include"),
    db: AsyncSession = Depends(get_db)
) -> list[ExtractorMetrics]:
    """
    Get metrics for all extractors.
    
    Returns success rates, average durations, and run counts.
    """
    since = datetime.utcnow() - timedelta(days=days)
    
    # Query extractor metrics
    query = select(
        Extractor.id,
        Extractor.name,
        Extractor.total_runs,
        Extractor.successful_runs,
        Extractor.failed_runs,
        Extractor.last_run_at,
        func.avg(ExtractorRun.duration_seconds).label("avg_duration")
    ).outerjoin(
        ExtractorRun,
        (ExtractorRun.extractor_id == Extractor.id) &
        (ExtractorRun.completed_at >= since) &
        (ExtractorRun.status == ExtractorStatus.SUCCESS)
    ).group_by(Extractor.id)
    
    result = await db.execute(query)
    rows = result.all()
    
    metrics = []
    for row in rows:
        success_rate = 0.0
        if row.total_runs > 0:
            success_rate = (row.successful_runs / row.total_runs) * 100
        
        metrics.append(ExtractorMetrics(
            extractor_id=row.id,
            extractor_name=row.name,
            total_runs=row.total_runs,
            successful_runs=row.successful_runs,
            failed_runs=row.failed_runs,
            success_rate=round(success_rate, 2),
            avg_duration_seconds=round(row.avg_duration, 2) if row.avg_duration else None,
            last_run_at=row.last_run_at
        ))
    
    return metrics


@router.get("/system", response_model=SystemMetricsResponse)
async def get_system_metrics(
    db: AsyncSession = Depends(get_db)
) -> SystemMetricsResponse:
    """
    Get current system-wide metrics.
    
    Returns overview of all extractors and active tasks.
    """
    # Count extractors by status
    extractor_counts = await db.execute(
        select(
            func.count(Extractor.id).label("total"),
            func.sum(case((Extractor.enabled == True, 1), else_=0)).label("enabled"),
            func.sum(case((Extractor.status == ExtractorStatus.RUNNING, 1), else_=0)).label("running")
        )
    )
    counts = extractor_counts.first()
    
    # Count active tasks (running in last 5 minutes)
    recent_time = datetime.utcnow() - timedelta(minutes=5)
    active_tasks = await db.execute(
        select(func.count())
        .where(
            (ExtractorRun.status == ExtractorStatus.RUNNING) &
            (ExtractorRun.started_at >= recent_time)
        )
    )
    
    # Calculate average duration and success rate for last 24 hours
    since_24h = datetime.utcnow() - timedelta(hours=24)
    stats = await db.execute(
        select(
            func.avg(ExtractorRun.duration_seconds).label("avg_duration"),
            func.count(ExtractorRun.id).label("total"),
            func.sum(case((ExtractorRun.status == ExtractorStatus.SUCCESS, 1), else_=0)).label("success")
        ).where(ExtractorRun.completed_at >= since_24h)
    )
    stats_row = stats.first()
    
    success_rate = None
    if stats_row.total and stats_row.total > 0:
        success_rate = (stats_row.success / stats_row.total) * 100
    
    return SystemMetricsResponse(
        timestamp=datetime.utcnow(),
        total_extractors=counts.total or 0,
        enabled_extractors=counts.enabled or 0,
        running_extractors=counts.running or 0,
        active_tasks=active_tasks.scalar() or 0,
        pending_tasks=0,  # Would need Celery introspection
        avg_duration_seconds=round(stats_row.avg_duration, 2) if stats_row.avg_duration else None,
        success_rate=round(success_rate, 2) if success_rate is not None else None,
        cpu_percent=None,  # Would need psutil
        memory_percent=None  # Would need psutil
    )


@router.get("/runs/recent", response_model=list)
async def get_recent_runs(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get recent extractor runs across all extractors."""
    result = await db.execute(
        select(ExtractorRun)
        .order_by(ExtractorRun.started_at.desc())
        .limit(limit)
    )
    runs = result.scalars().all()
    
    return [
        {
            "id": run.id,
            "extractor_name": run.extractor_name,
            "status": run.status,
            "started_at": run.started_at,
            "duration_seconds": run.duration_seconds,
            "items_extracted": run.items_extracted
        }
        for run in runs
    ]

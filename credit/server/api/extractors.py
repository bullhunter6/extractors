"""Extractor management API endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from server.core.database import get_db
from server.models import Extractor, ExtractorRun, ExtractorStatus, ExtractorCategory
from server.schemas import (
    ExtractorCreate,
    ExtractorUpdate,
    ExtractorResponse,
    ExtractorListResponse,
    ExtractorRunResponse,
    ExtractorRunListResponse,
    TaskTriggerRequest,
    TaskTriggerResponse,
)
from server.tasks.extractors import run_extractor
from server.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/extractors", tags=["extractors"])


@router.get("", response_model=ExtractorListResponse)
async def list_extractors(
    category: Optional[ExtractorCategory] = Query(None, description="Filter by category"),
    enabled: Optional[bool] = Query(None, description="Filter by enabled status"),
    status: Optional[ExtractorStatus] = Query(None, description="Filter by current status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Number of records to return"),
    db: AsyncSession = Depends(get_db)
) -> ExtractorListResponse:
    """
    List all extractors with optional filters.
    
    Returns paginated list of extractors.
    """
    query = select(Extractor)
    
    # Apply filters
    if category is not None:
        query = query.where(Extractor.category == category)
    if enabled is not None:
        query = query.where(Extractor.enabled == enabled)
    if status is not None:
        query = query.where(Extractor.status == status)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(skip).limit(limit).order_by(Extractor.name)
    
    result = await db.execute(query)
    extractors = result.scalars().all()
    
    return ExtractorListResponse(
        extractors=[ExtractorResponse.model_validate(e) for e in extractors],
        total=total
    )


@router.get("/{extractor_id}", response_model=ExtractorResponse)
async def get_extractor(
    extractor_id: int,
    db: AsyncSession = Depends(get_db)
) -> ExtractorResponse:
    """Get a specific extractor by ID."""
    result = await db.execute(
        select(Extractor).where(Extractor.id == extractor_id)
    )
    extractor = result.scalars().first()
    
    if not extractor:
        raise HTTPException(status_code=404, detail=f"Extractor {extractor_id} not found")
    
    return ExtractorResponse.model_validate(extractor)


@router.post("", response_model=ExtractorResponse, status_code=201)
async def create_extractor(
    extractor_data: ExtractorCreate,
    db: AsyncSession = Depends(get_db)
) -> ExtractorResponse:
    """Create a new extractor."""
    # Check if extractor with same name exists
    result = await db.execute(
        select(Extractor).where(Extractor.name == extractor_data.name)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail=f"Extractor with name '{extractor_data.name}' already exists"
        )
    
    extractor = Extractor(**extractor_data.model_dump())
    db.add(extractor)
    await db.commit()
    await db.refresh(extractor)
    
    logger.info("Extractor created", extractor_id=extractor.id, name=extractor.name)
    
    return ExtractorResponse.model_validate(extractor)


@router.patch("/{extractor_id}", response_model=ExtractorResponse)
async def update_extractor(
    extractor_id: int,
    update_data: ExtractorUpdate,
    db: AsyncSession = Depends(get_db)
) -> ExtractorResponse:
    """Update an extractor's configuration."""
    result = await db.execute(
        select(Extractor).where(Extractor.id == extractor_id)
    )
    extractor = result.scalars().first()
    
    if not extractor:
        raise HTTPException(status_code=404, detail=f"Extractor {extractor_id} not found")
    
    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(extractor, field, value)
    
    await db.commit()
    await db.refresh(extractor)
    
    logger.info("Extractor updated", extractor_id=extractor.id, fields=list(update_dict.keys()))
    
    return ExtractorResponse.model_validate(extractor)


@router.delete("/{extractor_id}", status_code=204)
async def delete_extractor(
    extractor_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete an extractor."""
    result = await db.execute(
        select(Extractor).where(Extractor.id == extractor_id)
    )
    extractor = result.scalars().first()
    
    if not extractor:
        raise HTTPException(status_code=404, detail=f"Extractor {extractor_id} not found")
    
    await db.delete(extractor)
    await db.commit()
    
    logger.info("Extractor deleted", extractor_id=extractor_id)


@router.post("/{extractor_id}/trigger", response_model=TaskTriggerResponse)
async def trigger_extractor(
    extractor_id: int,
    db: AsyncSession = Depends(get_db)
) -> TaskTriggerResponse:
    """Manually trigger an extractor to run."""
    result = await db.execute(
        select(Extractor).where(Extractor.id == extractor_id)
    )
    extractor = result.scalars().first()
    
    if not extractor:
        raise HTTPException(status_code=404, detail=f"Extractor {extractor_id} not found")
    
    if not extractor.enabled:
        raise HTTPException(status_code=400, detail="Extractor is disabled")
    
    if extractor.status == ExtractorStatus.RUNNING:
        raise HTTPException(status_code=409, detail="Extractor is already running")
    
    # Submit Celery task
    task = run_extractor.apply_async(
        kwargs={
            "extractor_id": extractor.id,
            "module_path": extractor.module_path,
            "function_name": extractor.function_name,
            "extractor_name": extractor.name
        }
    )
    
    # Update extractor status
    extractor.status = ExtractorStatus.RUNNING
    extractor.current_task_id = task.id
    await db.commit()
    
    # Create run record
    run = ExtractorRun(
        extractor_id=extractor.id,
        extractor_name=extractor.name,
        task_id=task.id,
        status=ExtractorStatus.RUNNING
    )
    db.add(run)
    await db.commit()
    
    logger.info(
        "Extractor triggered",
        extractor_id=extractor.id,
        task_id=task.id
    )
    
    return TaskTriggerResponse(
        task_id=task.id,
        extractor_id=extractor.id,
        extractor_name=extractor.name
    )


@router.post("/trigger-batch", response_model=list[TaskTriggerResponse])
async def trigger_batch(
    request: TaskTriggerRequest,
    db: AsyncSession = Depends(get_db)
) -> list[TaskTriggerResponse]:
    """Trigger multiple extractors to run."""
    responses = []
    
    for extractor_id in request.extractor_ids:
        try:
            response = await trigger_extractor(extractor_id, db)
            responses.append(response)
        except HTTPException as e:
            logger.warning(
                "Failed to trigger extractor",
                extractor_id=extractor_id,
                error=e.detail
            )
    
    return responses


@router.get("/{extractor_id}/runs", response_model=ExtractorRunListResponse)
async def list_extractor_runs(
    extractor_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
) -> ExtractorRunListResponse:
    """Get execution history for a specific extractor."""
    # Verify extractor exists
    result = await db.execute(
        select(Extractor).where(Extractor.id == extractor_id)
    )
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=f"Extractor {extractor_id} not found")
    
    # Get total count
    count_result = await db.execute(
        select(func.count()).where(ExtractorRun.extractor_id == extractor_id)
    )
    total = count_result.scalar() or 0
    
    # Get runs
    runs_result = await db.execute(
        select(ExtractorRun)
        .where(ExtractorRun.extractor_id == extractor_id)
        .order_by(desc(ExtractorRun.started_at))
        .offset(skip)
        .limit(limit)
    )
    runs = runs_result.scalars().all()
    
    return ExtractorRunListResponse(
        runs=[ExtractorRunResponse.model_validate(run) for run in runs],
        total=total
    )


@router.get("/{extractor_id}/runs/{run_id}/logs")
async def get_run_logs(
    extractor_id: int,
    run_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Get logs for a specific run."""
    result = await db.execute(
        select(ExtractorRun).where(
            ExtractorRun.id == run_id,
            ExtractorRun.extractor_id == extractor_id
        )
    )
    run = result.scalars().first()
    
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    
    return {
        "run_id": run.id,
        "extractor_id": run.extractor_id,
        "task_id": run.task_id,
        "status": run.status,
        "logs": run.logs or "",
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None
    }


@router.get("/{extractor_id}/stats")
async def get_extractor_stats(
    extractor_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Get detailed stats for a specific extractor."""
    result = await db.execute(
        select(Extractor).where(Extractor.id == extractor_id)
    )
    extractor = result.scalars().first()
    
    if not extractor:
        raise HTTPException(status_code=404, detail=f"Extractor {extractor_id} not found")
    
    # Get recent runs
    runs_result = await db.execute(
        select(ExtractorRun)
        .where(ExtractorRun.extractor_id == extractor_id)
        .order_by(desc(ExtractorRun.started_at))
        .limit(10)
    )
    recent_runs = runs_result.scalars().all()
    
    # Calculate success rate
    success_rate = 0.0
    if extractor.total_runs > 0:
        success_rate = (extractor.successful_runs / extractor.total_runs) * 100
    
    # Calculate average duration from recent runs
    avg_duration = 0.0
    durations = [r.duration_seconds for r in recent_runs if r.duration_seconds]
    if durations:
        avg_duration = sum(durations) / len(durations)
    
    return {
        "id": extractor.id,
        "name": extractor.name,
        "status": extractor.status.value if extractor.status else "idle",
        "category": extractor.category.value if extractor.category else None,
        "enabled": extractor.enabled,
        "total_runs": extractor.total_runs,
        "successful_runs": extractor.successful_runs,
        "failed_runs": extractor.failed_runs,
        "success_rate": round(success_rate, 2),
        "avg_duration_seconds": round(avg_duration, 2),
        "last_run_at": extractor.last_run_at.isoformat() if extractor.last_run_at else None,
        "last_success_at": extractor.last_success_at.isoformat() if extractor.last_success_at else None,
        "last_error": extractor.last_error,
        "current_task_id": extractor.current_task_id,
        "recent_runs": [
            {
                "id": r.id,
                "task_id": r.task_id,
                "status": r.status,
                "items_extracted": r.items_extracted,
                "duration_seconds": r.duration_seconds,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "error_message": r.error_message
            }
            for r in recent_runs
        ]
    }

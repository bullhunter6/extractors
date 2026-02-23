"""Pydantic schemas for API validation and serialization."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from server.models import ExtractorStatus, ExtractorCategory


# Extractor Schemas
class ExtractorBase(BaseModel):
    """Base extractor schema."""
    name: str = Field(..., description="Unique extractor name")
    display_name: str = Field(..., description="Human-readable display name")
    description: Optional[str] = Field(None, description="Extractor description")
    category: ExtractorCategory = Field(..., description="Extractor category")
    module_path: str = Field(..., description="Python module path")
    function_name: str = Field(..., description="Function name to call")


class ExtractorCreate(ExtractorBase):
    """Schema for creating a new extractor."""
    enabled: bool = Field(default=True, description="Whether extractor is enabled")
    schedule_interval_minutes: Optional[int] = Field(None, description="Run interval in minutes")
    timeout_seconds: int = Field(default=300, description="Task timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    retry_backoff_seconds: int = Field(default=60, description="Retry backoff in seconds")


class ExtractorUpdate(BaseModel):
    """Schema for updating an extractor."""
    display_name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    schedule_interval_minutes: Optional[int] = None
    timeout_seconds: Optional[int] = None
    max_retries: Optional[int] = None
    retry_backoff_seconds: Optional[int] = None


class ExtractorResponse(ExtractorBase):
    """Schema for extractor response."""
    id: int
    enabled: bool
    status: ExtractorStatus
    
    schedule_cron: Optional[str] = None
    schedule_interval_minutes: Optional[int] = None
    
    timeout_seconds: int
    max_retries: int
    retry_backoff_seconds: int
    
    current_task_id: Optional[str] = None
    
    total_runs: int
    successful_runs: int
    failed_runs: int
    
    last_run_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    last_error: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ExtractorListResponse(BaseModel):
    """Schema for list of extractors."""
    extractors: list[ExtractorResponse]
    total: int


# Extractor Run Schemas
class ExtractorRunResponse(BaseModel):
    """Schema for extractor run response."""
    id: int
    extractor_id: int
    extractor_name: str
    task_id: str
    status: ExtractorStatus
    
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    
    items_extracted: int
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    
    logs: Optional[str] = None
    
    worker_name: Optional[str] = None
    retry_count: int
    
    run_metadata: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)


class ExtractorRunListResponse(BaseModel):
    """Schema for list of extractor runs."""
    runs: list[ExtractorRunResponse]
    total: int


# Task Control Schemas
class TaskTriggerRequest(BaseModel):
    """Schema for manually triggering extractors."""
    extractor_ids: list[int] = Field(..., description="List of extractor IDs to run")


class TaskTriggerResponse(BaseModel):
    """Schema for task trigger response."""
    task_id: str
    extractor_id: int
    extractor_name: str
    status: str = "submitted"


class TaskStatusResponse(BaseModel):
    """Schema for task status response."""
    task_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
    traceback: Optional[str] = None


# Metrics Schemas
class ExtractorMetrics(BaseModel):
    """Schema for extractor-specific metrics."""
    extractor_id: int
    extractor_name: str
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    avg_duration_seconds: Optional[float] = None
    last_run_at: Optional[datetime] = None


class SystemMetricsResponse(BaseModel):
    """Schema for system metrics."""
    timestamp: datetime
    
    total_extractors: int
    enabled_extractors: int
    running_extractors: int
    
    active_tasks: int
    pending_tasks: int
    
    avg_duration_seconds: Optional[float] = None
    success_rate: Optional[float] = None
    
    cpu_percent: Optional[float] = None
    memory_percent: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)


# WebSocket Messages
class WSMessage(BaseModel):
    """WebSocket message schema."""
    type: str = Field(..., description="Message type")
    data: dict = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ExtractorStatusUpdate(BaseModel):
    """WebSocket extractor status update."""
    extractor_id: int
    extractor_name: str
    status: ExtractorStatus
    task_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

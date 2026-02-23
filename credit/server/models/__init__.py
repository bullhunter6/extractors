"""Database models for extractor management."""
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import String, Integer, Boolean, DateTime, Text, Enum, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column

from server.core.database import Base


class ExtractorStatus(str, PyEnum):
    """Extractor execution status."""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    DISABLED = "disabled"


class ExtractorCategory(str, PyEnum):
    """Extractor category."""
    BANKS_ME = "banks_me"
    BANKS_CA = "banks_ca"
    BANKS_CA_ME = "banks_ca_me"
    BANKS_RATING = "banks_rating"
    CORPORATES_ME = "corporates_me"
    CORPORATES_CA = "corporates_ca"
    CORPORATES_CA_ME = "corporates_ca_me"
    CORPORATES_RATING = "corporates_rating"
    SOVEREIGNS_ME = "sovereigns_me"
    SOVEREIGNS_CA = "sovereigns_ca"
    SOVEREIGNS_CA_ME = "sovereigns_ca_me"
    SOVEREIGNS_RATING = "sovereigns_rating"
    GLOBAL = "global"
    EVENTS = "events"
    PUBLICATIONS = "publications"
    METHODOLOGIES = "methodologies"


class Extractor(Base):
    """Extractor configuration model."""
    __tablename__ = "extractors"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    category: Mapped[ExtractorCategory] = mapped_column(
        Enum(ExtractorCategory),
        nullable=False,
        index=True
    )
    
    module_path: Mapped[str] = mapped_column(String(500), nullable=False)
    function_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[ExtractorStatus] = mapped_column(
        Enum(ExtractorStatus),
        default=ExtractorStatus.IDLE,
        nullable=False
    )
    
    # Scheduling
    schedule_cron: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    schedule_interval_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Task configuration
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=300, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    retry_backoff_seconds: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    
    # Current task info
    current_task_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Metrics
    total_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    successful_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class ExtractorRun(Base):
    """Extractor execution history."""
    __tablename__ = "extractor_runs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    extractor_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    extractor_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    task_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    
    status: Mapped[ExtractorStatus] = mapped_column(
        Enum(ExtractorStatus),
        default=ExtractorStatus.RUNNING,
        nullable=False
    )
    
    # Execution details
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Results
    items_extracted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_traceback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Logs - stored as text for persistence
    logs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    run_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Worker info
    worker_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class SystemMetrics(Base):
    """System-wide metrics snapshots."""
    __tablename__ = "system_metrics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    # Extractor metrics
    total_extractors: Mapped[int] = mapped_column(Integer, nullable=False)
    enabled_extractors: Mapped[int] = mapped_column(Integer, nullable=False)
    running_extractors: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Task metrics
    active_tasks: Mapped[int] = mapped_column(Integer, nullable=False)
    pending_tasks: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Performance
    avg_duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    success_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Resource usage
    cpu_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    memory_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

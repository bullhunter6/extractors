"""Celery application configuration."""
import sys
from pathlib import Path
from celery import Celery
from server.core.config import get_settings

# Add project root to Python path for extractor imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

settings = get_settings()

# Create Celery app
celery_app = Celery(
    "extractors",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["server.tasks.extractors", "server.tasks.scheduled"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.TASK_DEFAULT_TIMEOUT,
    task_soft_time_limit=settings.TASK_DEFAULT_TIMEOUT - 30,
    worker_prefetch_multiplier=4,  # Prefetch 4 tasks per worker thread
    worker_max_tasks_per_child=100,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=3600,  # 1 hour
    worker_concurrency=10,  # Default concurrency (can override with -c flag)
    beat_schedule={},  # Will be populated dynamically
    # Reduce logging verbosity
    worker_hijack_root_logger=False,
    worker_log_format="[%(asctime)s] [%(levelname)s] %(message)s",
    worker_task_log_format="[%(asctime)s] [%(levelname)s] %(task_name)s: %(message)s",
)

# Task routing - use default "celery" queue
celery_app.conf.task_routes = {
    "server.tasks.extractors.*": {"queue": "celery"},
    "server.tasks.scheduler.*": {"queue": "celery"},
}

# Set up the beat schedule immediately so Celery Beat picks it up on startup
from server.tasks.scheduler import setup_scheduler
setup_scheduler()

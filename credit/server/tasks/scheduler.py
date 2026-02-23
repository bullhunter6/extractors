"""Celery Beat scheduler for automated extractor execution."""
from datetime import timedelta
from celery.schedules import crontab
from server.core.celery_app import celery_app


def setup_scheduler():
    """
    Configure Celery Beat schedule for extractors.
    
    This should be called on application startup to dynamically
    configure schedules based on database extractor configurations.
    """
    # Poll every minute; run_scheduled_extractors checks per-extractor intervals internally
    celery_app.conf.beat_schedule = {
        'run-all-extractors-ticker': {
            'task': 'server.tasks.scheduler.run_scheduled_extractors',
            'schedule': timedelta(minutes=1),
        },
        'cleanup-old-runs': {
            'task': 'server.tasks.scheduler.cleanup_old_runs',
            'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        },
        'update-metrics': {
            'task': 'server.tasks.scheduler.update_system_metrics',
            'schedule': timedelta(minutes=5),
        },
    }


# Example: Category-specific schedules
CATEGORY_SCHEDULES = {
    'banks_rating': timedelta(minutes=30),  # Run rating actions more frequently
    'global': timedelta(hours=2),  # Run global less frequently
    'publications': timedelta(hours=6),  # Publications updated less often
    'events': timedelta(hours=3),  # Events medium frequency
}

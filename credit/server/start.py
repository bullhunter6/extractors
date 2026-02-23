"""Script to start all server components."""
import subprocess
import sys
import time
from pathlib import Path

def main():
    """Start FastAPI server, Celery worker, and Celery Beat."""
    print("=" * 60)
    print("Starting Extractor Control Server")
    print("=" * 60)
    
    # Check if Redis is running
    print("\n1. Checking Redis connection...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✓ Redis is running")
    except Exception as e:
        print("✗ Redis is not running!")
        print("  Please start Redis first:")
        print("  - Windows: docker run -d -p 6379:6379 redis")
        print("  - Linux/Mac: redis-server")
        return 1
    
    # Populate database
    print("\n2. Populating database...")
    try:
        subprocess.run([sys.executable, "-m", "server.utils.populate_db"], check=True)
        print("✓ Database populated")
    except subprocess.CalledProcessError:
        print("✗ Failed to populate database")
        return 1
    
    # Start services
    print("\n3. Starting services...")
    print("\nTo start all components, run these commands in separate terminals:\n")
    
    print("Terminal 1 - FastAPI Server:")
    print("  uvicorn server.main:app --reload --host 0.0.0.0 --port 8000\n")
    
    print("Terminal 2 - Celery Worker:")
    print("  celery -A server.core.celery_app worker --loglevel=info --pool=solo\n")
    
    print("Terminal 3 - Celery Beat (Scheduler):")
    print("  celery -A server.core.celery_app beat --loglevel=info\n")
    
    print("Terminal 4 - Flower (Monitoring) [Optional]:")
    print("  celery -A server.core.celery_app flower --port=5555\n")
    
    print("\nAccess Points:")
    print("  - API Docs: http://localhost:8000/docs")
    print("  - Dashboard: Open server/frontend/index.html in browser")
    print("  - Flower: http://localhost:5555 (if started)")
    print("\n" + "=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

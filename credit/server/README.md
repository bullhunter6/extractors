# Extractor Control Server

Production-ready FastAPI server for monitoring and controlling credit rating article extractors.

## Features

- **RESTful API** - Full CRUD operations for extractors
- **Celery Task Queue** - Isolated task execution with automatic retries
- **Real-time Updates** - WebSocket support for live status monitoring
- **SQLite Database** - Persistent storage of extractors, runs, and metrics
- **Structured Logging** - JSON logging with structlog
- **Metrics & Monitoring** - Track success rates, durations, and system health

## Architecture

```
server/
├── main.py                 # FastAPI application
├── core/
│   ├── config.py          # Settings with pydantic-settings
│   ├── database.py        # SQLAlchemy async setup
│   ├── logging.py         # Structured logging
│   └── celery_app.py      # Celery configuration
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas
├── api/
│   ├── extractors.py      # Extractor CRUD endpoints
│   ├── metrics.py         # Metrics endpoints
│   └── websocket.py       # WebSocket endpoint
├── tasks/
│   └── extractors.py      # Celery tasks
└── utils/
    └── populate_db.py     # Database population script
```

## Prerequisites

- Python 3.12+
- Redis server (for Celery broker)

## Installation

1. **Install dependencies:**
```bash
pip install -r server/requirements.txt
```

2. **Start Redis:**
```bash
# Windows (using WSL or Docker)
docker run -d -p 6379:6379 redis

# Or use WSL
redis-server
```

3. **Populate database:**
```bash
python -m server.utils.populate_db
```

## Running the Server

### 1. Start FastAPI Server

```bash
# Development mode with auto-reload
python -m server.main

# Or with uvicorn directly
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Celery Worker

```bash
celery -A server.core.celery_app worker --loglevel=info --pool=solo
```

### 3. (Optional) Start Flower for Monitoring

```bash
celery -A server.core.celery_app flower --port=5555
```

### 4. (Optional) Start Celery Beat for Scheduling

```bash
celery -A server.core.celery_app beat --loglevel=info
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Extractors
- `GET /api/v1/extractors` - List all extractors
- `GET /api/v1/extractors/{id}` - Get extractor details
- `POST /api/v1/extractors/{id}/trigger` - Manually run extractor
- `PATCH /api/v1/extractors/{id}` - Update extractor config
- `GET /api/v1/extractors/{id}/runs` - Get execution history

#### Metrics
- `GET /api/v1/metrics/extractors` - Get per-extractor metrics
- `GET /api/v1/metrics/system` - Get system-wide metrics
- `GET /api/v1/metrics/runs/recent` - Get recent runs

#### WebSocket
- `WS /ws/status` - Real-time status updates

## Configuration

Create a `.env` file in the project root:

```env
# API Settings
API_TITLE="Extractor Control API"
API_VERSION="1.0.0"
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite+aiosqlite:///./extractors.db

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/1

# Logging
LOG_LEVEL=INFO

# CORS (for frontend)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Task Settings
TASK_DEFAULT_TIMEOUT=300
TASK_MAX_RETRIES=3
TASK_RETRY_BACKOFF=60
```

## Usage Examples

### Trigger Single Extractor

```python
import requests

response = requests.post("http://localhost:8000/api/v1/extractors/1/trigger")
print(response.json())
# {"task_id": "abc-123", "extractor_id": 1, "status": "submitted"}
```

### Trigger Multiple Extractors

```python
response = requests.post(
    "http://localhost:8000/api/v1/extractors/trigger-batch",
    json={"extractor_ids": [1, 2, 3]}
)
```

### Get Metrics

```python
response = requests.get("http://localhost:8000/api/v1/metrics/extractors?days=7")
metrics = response.json()
```

### WebSocket Connection (JavaScript)

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/status");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Status update:", data);
};
```

## Development

### Running Tests

```bash
pytest server/tests/
```

### Code Quality

```bash
# Type checking
mypy server/

# Linting
ruff check server/

# Formatting
black server/
```

## Production Deployment

For production, use:

```bash
# Gunicorn with Uvicorn workers
gunicorn server.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Celery with multiple workers
celery -A server.core.celery_app worker --loglevel=info --concurrency=4
```

## Monitoring

- **Flower Dashboard**: http://localhost:5555
- **Application Logs**: `~/news-extractor/logs/`
- **Celery Task States**: Via Flower or Redis CLI

## Troubleshooting

### Redis Connection Error
```
# Verify Redis is running
redis-cli ping
# Should return PONG
```

### Import Errors
```bash
# Make sure you're in the project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Locked
```bash
# If SQLite is locked, stop all processes and restart
pkill -f "celery|uvicorn"
```

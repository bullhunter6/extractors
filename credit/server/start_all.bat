@echo off
echo Starting all server components...

start "FastAPI Server" cmd /k "venv\Scripts\activate && uvicorn server.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 >nul

start "Celery Worker" cmd /k "venv\Scripts\activate && celery -A server.core.celery_app worker --loglevel=info --pool=solo"
timeout /t 3 >nul

start "Celery Beat" cmd /k "venv\Scripts\activate && celery -A server.core.celery_app beat --loglevel=info"
timeout /t 2 >nul

echo.
echo All components started!
echo.
echo API Docs: http://localhost:8000/docs
echo Dashboard: server\frontend\index.html
echo.
echo Close this window to keep servers running.
pause

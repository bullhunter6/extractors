@echo off
echo ============================================================
echo Extractor Control Server - Windows Startup Script
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please create it first: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r server\requirements.txt -q

REM Populate database
echo.
echo Populating database...
python -m server.utils.populate_db

echo.
echo ============================================================
echo Server components ready to start
echo ============================================================
echo.
echo Run these commands in separate terminal windows:
echo.
echo   1. uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
echo   2. celery -A server.core.celery_app worker --loglevel=info --pool=solo
echo   3. celery -A server.core.celery_app beat --loglevel=info
echo.
echo Or use start_all.bat to start all in separate windows
echo.
echo ============================================================

pause

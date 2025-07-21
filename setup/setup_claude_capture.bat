@echo off
echo [INFO] Claude Capture System - Setup and Install Dependencies
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [SUCCESS] Python is available:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found. Please install pip first.
    pause
    exit /b 1
)

echo [SUCCESS] pip is available:
pip --version
echo.

echo [INFO] Installing required Python packages...
echo.

REM Install required packages
echo [INFO] Installing watchdog...
pip install watchdog

echo.
echo [INFO] Installing psutil...
pip install psutil

echo.
echo [INFO] Installing sqlite3 (usually included with Python)...
python -c "import sqlite3; print('sqlite3 is available')" 2>nul || pip install pysqlite3

echo.
echo [INFO] Testing all dependencies...
echo.

REM Test all imports
python -c "
import sys
import os
import json
import sqlite3
import time
import threading
from datetime import datetime
from pathlib import Path

try:
    import watchdog
    print('[SUCCESS] watchdog imported successfully')
except ImportError as e:
    print('[ERROR] watchdog import failed:', e)
    sys.exit(1)

try:
    import psutil
    print('[SUCCESS] psutil imported successfully')
except ImportError as e:
    print('[ERROR] psutil import failed:', e)
    sys.exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print('[SUCCESS] watchdog components imported successfully')
except ImportError as e:
    print('[ERROR] watchdog components import failed:', e)
    sys.exit(1)

print('[SUCCESS] All dependencies are working!')
"

if %errorlevel% neq 0 (
    echo [ERROR] Dependency test failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All dependencies installed and tested successfully!
echo.
echo [INFO] Now starting Claude capture system...
echo.

REM Start the capture system
python claude_capture\integrations\seamless_claude_integration.py --start

echo.
echo [SUCCESS] Setup complete! Claude capture system is now running.
echo [INFO] You can now use Claude normally - everything will be captured automatically
echo.
echo Useful commands:
echo   Check status: python claude_capture\integrations\seamless_claude_integration.py --status
echo   Stop capture: python claude_capture\integrations\seamless_claude_integration.py --integrate
echo   Run test: python claude_capture\tests\test_capture_windows.py
echo.
pause
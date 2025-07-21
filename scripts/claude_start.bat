@echo off
echo [INFO] Claude Capture System - Simple Start
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

echo [SUCCESS] Python is available
echo.

REM Check if integration file exists
if not exist "claude_capture\integrations\seamless_claude_integration.py" (
    echo [ERROR] Integration file not found: claude_capture\integrations\seamless_claude_integration.py
    echo [INFO] Make sure you're in the correct directory with the claude_capture folder
    pause
    exit /b 1
)

echo [SUCCESS] Integration file found
echo.

REM Start the capture system
echo [INFO] Starting Claude capture system...
echo [INFO] This will run in the background and capture all Claude conversations
echo.

python claude_capture\integrations\seamless_claude_integration.py --start

echo.
echo [SUCCESS] Capture system started!
echo [INFO] You can now use Claude normally - everything will be captured automatically
echo.
echo To check status: python claude_capture\integrations\seamless_claude_integration.py --status
echo To stop: python claude_capture\integrations\seamless_claude_integration.py --integrate
echo.
pause
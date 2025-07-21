@echo off
echo [INFO] Claude Capture System - Windows Compatible
echo ==========================================
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

REM Try the Windows-compatible version first
if exist "claude_capture\integrations\seamless_claude_integration_windows.py" (
    echo [INFO] Using Windows-compatible version...
    python claude_capture\integrations\seamless_claude_integration_windows.py --start
) else (
    echo [INFO] Using standard version...
    python claude_capture\integrations\seamless_claude_integration.py --start
)

echo.
echo [SUCCESS] Claude capture system started!
echo [INFO] You can now use Claude normally - everything will be captured automatically
echo.
pause
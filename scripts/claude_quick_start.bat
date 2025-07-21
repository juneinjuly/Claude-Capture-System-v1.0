@echo off
echo [INFO] Claude Capture Manager - Quick Start for Windows
echo ============================================================
echo.
echo This script helps you get started with Claude capture on Windows.
echo.
echo Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found:
python --version

REM Check if claude_capture folder exists
if not exist "claude_capture" (
    echo [ERROR] claude_capture folder not found.
    echo Please make sure you're in the correct directory.
    pause
    exit /b 1
)

echo [OK] claude_capture folder found

REM Check integration file
if not exist "claude_capture\integrations\seamless_claude_integration.py" (
    echo [ERROR] Integration file not found.
    echo Expected: claude_capture\integrations\seamless_claude_integration.py
    pause
    exit /b 1
)

echo [OK] Integration file found

echo.
echo ============================================================
echo System check complete! You can now use:
echo.
echo Option 1 - PowerShell (Recommended):
echo   .\claude_capture_manager.ps1 start
echo   .\claude_capture_manager.ps1 status
echo   .\claude_capture_manager.ps1 search "your query"
echo.
echo Option 2 - Batch files:
echo   claude_capture\scripts\start_auto_capture.bat
echo.
echo Option 3 - Direct Python:
echo   python claude_capture\integrations\seamless_claude_integration.py --start
echo.
echo ============================================================
echo.
echo Would you like to start the capture system now? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo [INFO] Starting capture system...
    python claude_capture\integrations\seamless_claude_integration.py --start
    echo.
    echo [SUCCESS] Capture system started!
    echo You can now use Claude normally - everything will be captured automatically.
) else (
    echo [INFO] You can start the capture system later using the commands above.
)

echo.
pause
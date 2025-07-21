@echo off
REM Claude Capture System - Main Launcher
REM Quick access to all Claude capture functionality

if "%1"=="test" (
    echo [INFO] Running Claude capture test...
    call claude_capture\scripts\claude_test_simple.bat
    goto :end
)

if "%1"=="start" (
    echo [INFO] Starting Claude capture system...
    call claude_capture\scripts\claude_start_simple.bat
    goto :end
)

if "%1"=="status" (
    echo [INFO] Checking Claude capture status...
    python claude_capture\integrations\seamless_claude_integration_windows.py --status
    goto :end
)

if "%1"=="help" (
    goto :help
)

if "%1"=="" (
    goto :help
)

echo [ERROR] Unknown command: %1
goto :help

:help
echo Claude Capture System - Main Launcher
echo ====================================
echo.
echo Usage: claude [command]
echo.
echo Commands:
echo   test     - Run system test
echo   start    - Start capture system
echo   status   - Check system status
echo   help     - Show this help
echo.
echo Examples:
echo   claude test     # Test the system
echo   claude start    # Start capturing
echo   claude status   # Check status
echo.
echo Files:
echo   claude_capture\scripts\     - All management scripts
echo   claude_capture\tests\       - Test files
echo   claude_capture\setup\       - Setup and installation
echo   claude_capture\docs\        - Documentation
echo.

:end
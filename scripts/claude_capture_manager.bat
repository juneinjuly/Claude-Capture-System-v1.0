@echo off
REM Claude Capture Manager - Windows version

echo [INFO] Claude Capture Manager - Organized File Access
echo ============================================================

if "%1"=="start" (
    echo [INFO] Starting Claude capture system...
    claude_capture\scripts\start_auto_capture.bat
    goto :end
)

if "%1"=="stop" (
    echo [INFO] Stopping Claude capture system...
    python claude_capture\integrations\seamless_claude_integration.py --integrate
    echo [INFO] Capture system stopped
    goto :end
)

if "%1"=="status" (
    echo [INFO] Checking capture status...
    python claude_capture\integrations\seamless_claude_integration.py --status
    goto :end
)

if "%1"=="search" (
    if "%2"=="" (
        echo [ERROR] Please provide a search query
        echo Usage: %0 search "your query"
        goto :end
    )
    echo [INFO] Searching conversations...
    python claude_capture\integrations\claude_code_integration.py --search "%2"
    goto :end
)

if "%1"=="analytics" (
    echo [INFO] Viewing analytics...
    python claude_capture\integrations\claude_code_integration.py --analytics
    goto :end
)

if "%1"=="test" (
    echo [INFO] Running capture system test...
    python claude_capture\tests\test_capture_windows.py
    goto :end
)

if "%1"=="list" (
    echo [INFO] Claude Capture File Organization:
    echo.
    echo Scripts:
    dir /B claude_capture\scripts\*.sh claude_capture\scripts\*.bat 2>nul
    echo.
    echo Integrations:
    dir /B claude_capture\integrations\*.py 2>nul
    echo.
    echo Tests:
    dir /B claude_capture\tests\*.py claude_capture\tests\*.sh 2>nul
    echo.
    echo Documentation:
    dir /B claude_capture\docs\*.md 2>nul
    goto :end
)

if "%1"=="open" (
    echo [INFO] Opening claude_capture folder...
    explorer claude_capture
    goto :end
)

REM Show usage
echo.
echo Usage: %0 [command] [options]
echo.
echo Commands:
echo   start          - Start automatic capture
echo   stop           - Stop automatic capture
echo   status         - Check capture status
echo   search ^<query^> - Search captured conversations
echo   analytics      - View analytics
echo   test           - Run capture system test
echo   list           - List all organized files
echo   open           - Open claude_capture folder
echo.
echo Examples:
echo   %0 start                      # Start capture
echo   %0 search "RSI strategy"       # Search conversations
echo   %0 analytics                  # View analytics
echo   %0 test                       # Test system

:end
pause
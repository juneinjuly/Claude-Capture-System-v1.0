@echo off
echo [INFO] Claude Files Organization
echo ============================
echo.
echo This script will organize all Claude-related files into proper folders.
echo.
echo Before:
echo   - Files scattered in project root
echo   - Mixed file types
echo   - Hard to find specific files
echo.
echo After:
echo   - claude_capture/scripts/     (All management scripts)
echo   - claude_capture/tests/       (All test files)
echo   - claude_capture/setup/       (Installation scripts)
echo   - claude_capture/docs/        (Documentation)
echo   - Quick launchers in root
echo.
echo Continue? (y/n)
set /p choice=
if /i not "%choice%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo [INFO] Starting organization...
python organize_claude_files.py

echo.
echo [INFO] Organization complete!
echo.
echo You can now use:
echo   .\claude_launcher.bat                 (Quick launcher)
echo   .\claude_capture\scripts\claude_start.bat  (Direct start)
echo.
pause
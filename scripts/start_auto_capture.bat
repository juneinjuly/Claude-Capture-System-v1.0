@echo off
REM Windows version of auto-capture start script

echo [INFO] Starting Claude Code Integration for Windows...
echo [INFO] This will automatically capture all your conversations with Claude
echo [INFO] No manual commands needed - just use Claude normally!

REM Check if already running
tasklist /FI "IMAGENAME eq python.exe" /FO CSV | findstr /C:"seamless_claude_integration.py" >nul
if %errorlevel% == 0 (
    echo [INFO] Seamless Claude integration already running
    python ../integrations/seamless_claude_integration.py --status
    goto :end
)

REM Start the integration
echo [INFO] Starting seamless Claude Code integration...
python ../integrations/seamless_claude_integration.py --start

:end
pause
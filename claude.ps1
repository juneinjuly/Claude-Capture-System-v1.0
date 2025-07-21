# Claude Capture System - PowerShell Launcher
param(
    [string]$Command = ""
)

switch ($Command.ToLower()) {
    "test" {
        Write-Host "[INFO] Running Claude capture test..." -ForegroundColor Blue
        & ".\claude_capture\scripts\claude_test_simple.bat"
    }
    "start" {
        Write-Host "[INFO] Starting Claude capture system..." -ForegroundColor Blue
        & ".\claude_capture\scripts\claude_start_simple.bat"
    }
    "status" {
        Write-Host "[INFO] Checking Claude capture status..." -ForegroundColor Blue
        python claude_capture\integrations\seamless_claude_integration_windows.py --status
    }
    "help" {
        Write-Host "Claude Capture System - PowerShell Launcher" -ForegroundColor Magenta
        Write-Host "===========================================" -ForegroundColor Magenta
        Write-Host ""
        Write-Host "Usage: .\claude [command]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Green
        Write-Host "  test     - Run system test"
        Write-Host "  start    - Start capture system"
        Write-Host "  status   - Check system status"
        Write-Host "  help     - Show this help"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Green
        Write-Host "  .\claude test     # Test the system"
        Write-Host "  .\claude start    # Start capturing"
        Write-Host "  .\claude status   # Check status"
        Write-Host ""
        Write-Host "Files:" -ForegroundColor Green
        Write-Host "  claude_capture\scripts\     - All management scripts"
        Write-Host "  claude_capture\tests\       - Test files"
        Write-Host "  claude_capture\setup\       - Setup and installation"
        Write-Host "  claude_capture\docs\        - Documentation"
        Write-Host ""
    }
    default {
        if ($Command -eq "") {
            Write-Host "Claude Capture System - PowerShell Launcher" -ForegroundColor Magenta
            Write-Host "===========================================" -ForegroundColor Magenta
            Write-Host ""
            Write-Host "Usage: .\claude [command]" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Quick commands:" -ForegroundColor Green
            Write-Host "  .\claude test     # Test the system"
            Write-Host "  .\claude start    # Start capturing"
            Write-Host "  .\claude status   # Check status"
            Write-Host "  .\claude help     # Show full help"
            Write-Host ""
        } else {
            Write-Host "[ERROR] Unknown command: $Command" -ForegroundColor Red
            Write-Host "Use '.\claude help' to see available commands" -ForegroundColor Yellow
        }
    }
}
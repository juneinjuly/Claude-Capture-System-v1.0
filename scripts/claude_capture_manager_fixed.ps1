# Claude Capture Manager - PowerShell version (Fixed)
param(
    [string]$Command = "",
    [string]$Query = ""
)

function Print-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Print-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Print-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Print-Claude {
    param([string]$Message)
    Write-Host "[CLAUDE] $Message" -ForegroundColor Magenta
}

function Show-Usage {
    Write-Host "Claude Capture Manager - Organized File Access" -ForegroundColor Magenta
    Write-Host "============================================================"
    Write-Host ""
    Write-Host "Usage: .\claude_capture_manager_fixed.ps1 [command] [options]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  start          - Start automatic capture"
    Write-Host "  stop           - Stop automatic capture"
    Write-Host "  status         - Check capture status"
    Write-Host "  search <query> - Search captured conversations"
    Write-Host "  analytics      - View analytics"
    Write-Host "  test           - Run capture system test"
    Write-Host "  list           - List all organized files"
    Write-Host "  open           - Open claude_capture folder"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\claude_capture_manager_fixed.ps1 start"
    Write-Host "  .\claude_capture_manager_fixed.ps1 search 'RSI strategy'"
    Write-Host "  .\claude_capture_manager_fixed.ps1 status"
    Write-Host ""
}

function Start-Capture {
    Print-Info "Starting Claude capture system..."
    
    # Check if Python is available
    try {
        $pythonVersion = python --version 2>&1
        Print-Success "Python found: $pythonVersion"
    }
    catch {
        Print-Warning "Python not found. Please install Python first."
        return
    }
    
    # Check if integration file exists
    $integrationFile = "claude_capture\integrations\seamless_claude_integration.py"
    if (Test-Path $integrationFile) {
        Print-Success "Found integration file: $integrationFile"
        
        # Check if already running
        $runningProcesses = Get-Process python -ErrorAction SilentlyContinue
        $claudeProcess = $runningProcesses | Where-Object { $_.MainWindowTitle -like "*seamless_claude_integration*" -or $_.ProcessName -eq "python" }
        
        if ($claudeProcess) {
            Print-Info "Claude integration may already be running"
            python $integrationFile --status
            return
        }
        
        # Start the integration
        Print-Info "Starting seamless Claude Code integration..."
        Print-Info "This will automatically capture all your conversations with Claude"
        Print-Info "No manual commands needed - just use Claude normally!"
        
        # Start background process
        $process = Start-Process -FilePath "python" -ArgumentList "$integrationFile --start" -WindowStyle Hidden -PassThru
        
        Start-Sleep -Seconds 3
        
        if ($process -and !$process.HasExited) {
            Print-Success "Seamless Claude integration started successfully!"
            Print-Success "Process ID: $($process.Id)"
            Print-Info "Auto-capture mode: ACTIVE"
            Print-Info "All conversations will be automatically captured"
            Print-Info "File monitoring: ENABLED"
            Print-Info "Use '.\claude_capture_manager_fixed.ps1 status' to see activity"
            Print-Info "Use '.\claude_capture_manager_fixed.ps1 stop' to stop"
            Print-Success "Just ask questions and the system captures everything"
        } else {
            Print-Warning "Failed to start integration process"
        }
        
    } else {
        Print-Warning "Integration file not found: $integrationFile"
        Print-Info "Please make sure the claude_capture folder is properly set up."
    }
}

function Stop-Capture {
    Print-Info "Stopping Claude capture system..."
    
    # Kill any running processes
    $processes = Get-Process python -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($proc in $processes) {
            try {
                $commandLine = (Get-WmiObject Win32_Process -Filter "ProcessId = $($proc.Id)").CommandLine
                if ($commandLine -like "*seamless_claude_integration*") {
                    Print-Info "Stopping process PID: $($proc.Id)"
                    Stop-Process -Id $proc.Id -Force
                }
            } catch {
                # Continue if we can't get command line
            }
        }
    }
    
    # Run final integration
    $integrationFile = "claude_capture\integrations\seamless_claude_integration.py"
    if (Test-Path $integrationFile) {
        python $integrationFile --integrate
    }
    
    Print-Success "Seamless Claude integration stopped"
    Print-Info "Final integration completed"
}

function Get-Status {
    Print-Info "Checking capture status..."
    
    # Check if processes are running
    $processes = Get-Process python -ErrorAction SilentlyContinue
    $claudeProcesses = @()
    
    if ($processes) {
        foreach ($proc in $processes) {
            try {
                $commandLine = (Get-WmiObject Win32_Process -Filter "ProcessId = $($proc.Id)").CommandLine
                if ($commandLine -like "*seamless_claude_integration*") {
                    $claudeProcesses += $proc
                }
            } catch {
                # Continue if we can't get command line
            }
        }
    }
    
    if ($claudeProcesses.Count -gt 0) {
        $pids = $claudeProcesses | ForEach-Object { $_.Id }
        Print-Success "Auto-capture process running (PID: $($pids -join ', '))"
        
        # Get detailed status
        $integrationFile = "claude_capture\integrations\seamless_claude_integration.py"
        if (Test-Path $integrationFile) {
            Print-Info "Getting detailed status..."
            python $integrationFile --status
        }
    } else {
        Print-Warning "Auto-capture process not running"
        Print-Info "Start with: .\claude_capture_manager_fixed.ps1 start"
    }
    
    # Check for database files
    Print-Info "Checking database files..."
    if (Test-Path "claude_auto_capture.db") {
        Print-Success "Database file exists: claude_auto_capture.db"
    } else {
        Print-Warning "Database file not found: claude_auto_capture.db"
    }
    
    if (Test-Path "claude_session_state.json") {
        Print-Success "Session state file exists: claude_session_state.json"
    } else {
        Print-Warning "Session state file not found: claude_session_state.json"
    }
}

function Search-Conversations {
    param([string]$SearchQuery)
    
    if (-not $SearchQuery) {
        Print-Warning "Please provide a search query"
        Write-Host "Usage: .\claude_capture_manager_fixed.ps1 search 'your query'"
        return
    }
    
    Print-Info "Searching conversations for: $SearchQuery"
    $integrationFile = "claude_capture\integrations\claude_code_integration.py"
    if (Test-Path $integrationFile) {
        python $integrationFile --search $SearchQuery
    } else {
        Print-Warning "Integration file not found: $integrationFile"
    }
}

function Show-Analytics {
    Print-Info "Viewing analytics..."
    $integrationFile = "claude_capture\integrations\claude_code_integration.py"
    if (Test-Path $integrationFile) {
        python $integrationFile --analytics
    } else {
        Print-Warning "Integration file not found: $integrationFile"
    }
}

function Test-System {
    Print-Info "Running capture system test..."
    $testFile = "claude_capture\tests\test_capture_windows.py"
    if (Test-Path $testFile) {
        python $testFile
    } else {
        Print-Warning "Test file not found: $testFile"
        Print-Info "Creating quick test..."
        
        # Create a simple test file
        $testContent = @"
# PowerShell Test File for Claude Capture
# This file should trigger the capture system

from AlgorithmImports import *

class PowerShellTestAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.Log("PowerShell test file created")
        self.Log("Testing Claude capture system from Windows PowerShell")
"@
        
        $testContent | Out-File -FilePath "powershell_test_claude.py" -Encoding UTF8
        Print-Success "Created test file: powershell_test_claude.py"
        Print-Info "If capture system is working, you should see activity notifications"
    }
}

function Show-FileList {
    Print-Info "Claude Capture File Organization:"
    Write-Host ""
    
    Print-Claude "Scripts:"
    if (Test-Path "claude_capture\scripts") {
        Get-ChildItem "claude_capture\scripts" -Filter "*.sh" | ForEach-Object { Write-Host "   $($_.Name)" }
        Get-ChildItem "claude_capture\scripts" -Filter "*.bat" | ForEach-Object { Write-Host "   $($_.Name)" }
    }
    
    Write-Host ""
    Print-Claude "Integrations:"
    if (Test-Path "claude_capture\integrations") {
        Get-ChildItem "claude_capture\integrations" -Filter "*.py" | ForEach-Object { Write-Host "   $($_.Name)" }
    }
    
    Write-Host ""
    Print-Claude "Tests:"
    if (Test-Path "claude_capture\tests") {
        Get-ChildItem "claude_capture\tests" -Filter "*.py" | ForEach-Object { Write-Host "   $($_.Name)" }
        Get-ChildItem "claude_capture\tests" -Filter "*.sh" | ForEach-Object { Write-Host "   $($_.Name)" }
    }
    
    Write-Host ""
    Print-Claude "Documentation:"
    if (Test-Path "claude_capture\docs") {
        Get-ChildItem "claude_capture\docs" -Filter "*.md" | ForEach-Object { Write-Host "   $($_.Name)" }
    }
}

function Open-Folder {
    Print-Info "Opening claude_capture folder..."
    if (Test-Path "claude_capture") {
        Start-Process explorer "claude_capture"
    } else {
        Print-Warning "claude_capture folder not found"
    }
}

# Main script logic
switch ($Command.ToLower()) {
    "start" { Start-Capture }
    "stop" { Stop-Capture }
    "status" { Get-Status }
    "search" { Search-Conversations -SearchQuery $Query }
    "analytics" { Show-Analytics }
    "test" { Test-System }
    "list" { Show-FileList }
    "open" { Open-Folder }
    default { Show-Usage }
}
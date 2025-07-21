#!/usr/bin/env python3
"""
Claude Files Organization Script
Cleans up and organizes all Claude-related files into proper folder structure
"""

import os
import shutil
from pathlib import Path
import time

def organize_claude_files():
    """Organize all Claude-related files into proper structure"""
    
    print("🧹 CLAUDE FILES ORGANIZATION SCRIPT")
    print("=" * 50)
    
    # Get current directory
    root_dir = Path.cwd()
    print(f"📁 Working directory: {root_dir}")
    
    # Define target directories
    claude_dir = root_dir / "claude_capture"
    scripts_dir = claude_dir / "scripts"
    tests_dir = claude_dir / "tests"
    setup_dir = claude_dir / "setup"
    docs_dir = claude_dir / "docs"
    
    # Create directories if they don't exist
    directories = [claude_dir, scripts_dir, tests_dir, setup_dir, docs_dir]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"📁 Ensured directory exists: {directory}")
    
    print("\n🔄 MOVING FILES TO APPROPRIATE FOLDERS...")
    
    # Files to move to scripts/
    script_files = [
        "claude_capture_manager.sh",
        "claude_capture_manager.bat", 
        "claude_capture_manager.ps1",
        "claude_capture_manager_fixed.ps1",
        "claude_start.bat",
        "claude_quick_start.bat"
    ]
    
    # Files to move to tests/
    test_files = [
        "test_claude_capture.py",
        "test_claude_capture.bat",
        "claude_test_from_root.py",
        "test_powershell.ps1"
    ]
    
    # Files to move to setup/
    setup_files = [
        "setup_claude_capture.bat",
        "install_dependencies.bat",
        "requirements.txt"
    ]
    
    # Files to move to docs/
    doc_files = [
        "ZERO_COMMAND_SETUP.md"
    ]
    
    # Database files to keep in root but document
    database_files = [
        "claude_auto_capture.db",
        "claude_session_state.json"
    ]
    
    # Move script files
    print("\n📜 Moving script files...")
    for file_name in script_files:
        src = root_dir / file_name
        dst = scripts_dir / file_name
        if src.exists():
            if dst.exists():
                print(f"⚠️  {file_name} already exists in scripts/, skipping")
            else:
                shutil.move(str(src), str(dst))
                print(f"✅ Moved {file_name} → scripts/")
        else:
            print(f"⚠️  {file_name} not found, skipping")
    
    # Move test files
    print("\n🧪 Moving test files...")
    for file_name in test_files:
        src = root_dir / file_name
        dst = tests_dir / file_name
        if src.exists():
            if dst.exists():
                print(f"⚠️  {file_name} already exists in tests/, skipping")
            else:
                shutil.move(str(src), str(dst))
                print(f"✅ Moved {file_name} → tests/")
        else:
            print(f"⚠️  {file_name} not found, skipping")
    
    # Move setup files
    print("\n🔧 Moving setup files...")
    for file_name in setup_files:
        src = root_dir / file_name
        dst = setup_dir / file_name
        if src.exists():
            if dst.exists():
                print(f"⚠️  {file_name} already exists in setup/, skipping")
            else:
                shutil.move(str(src), str(dst))
                print(f"✅ Moved {file_name} → setup/")
        else:
            print(f"⚠️  {file_name} not found, skipping")
    
    # Move documentation files
    print("\n📖 Moving documentation files...")
    for file_name in doc_files:
        src = root_dir / file_name
        dst = docs_dir / file_name
        if src.exists():
            if dst.exists():
                print(f"⚠️  {file_name} already exists in docs/, skipping")
            else:
                shutil.move(str(src), str(dst))
                print(f"✅ Moved {file_name} → docs/")
        else:
            print(f"⚠️  {file_name} not found, skipping")
    
    # Clean up temporary files
    print("\n🗑️  Cleaning up temporary files...")
    temp_patterns = ["*.tmp.*", "*.py.tmp.*"]
    for pattern in temp_patterns:
        for temp_file in root_dir.glob(pattern):
            temp_file.unlink()
            print(f"🗑️  Removed: {temp_file.name}")
    
    # Check database files
    print("\n💾 Checking database files...")
    for file_name in database_files:
        file_path = root_dir / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file_name}: {size} bytes (keeping in root)")
        else:
            print(f"⚠️  {file_name}: Not found")
    
    # Create quick access scripts in root
    print("\n🚀 Creating quick access scripts...")
    
    # Create main launcher script
    launcher_content = """#!/bin/bash
# Claude Capture Quick Launcher
# This script provides easy access to all Claude capture functionality

echo "🤖 Claude Capture System - Quick Launcher"
echo "========================================"
echo ""
echo "Choose an option:"
echo "1. Start capture system"
echo "2. Check status"
echo "3. Run tests"
echo "4. Open file manager"
echo "5. View documentation"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1) ./claude_capture/scripts/claude_start.bat ;;
    2) python claude_capture/integrations/seamless_claude_integration.py --status ;;
    3) python claude_capture/tests/claude_test_from_root.py ;;
    4) ./claude_capture/scripts/claude_capture_manager_fixed.ps1 open ;;
    5) cat claude_capture/docs/ZERO_COMMAND_SETUP.md ;;
    *) echo "Invalid option" ;;
esac
"""
    
    with open(root_dir / "claude_launcher.sh", 'w') as f:
        f.write(launcher_content)
    
    # Create Windows batch launcher
    bat_launcher_content = """@echo off
echo [INFO] Claude Capture System - Quick Launcher
echo =======================================
echo.
echo Choose an option:
echo 1. Start capture system
echo 2. Check status  
echo 3. Run tests
echo 4. Setup dependencies
echo 5. Open folder
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" call claude_capture\\scripts\\claude_start.bat
if "%choice%"=="2" python claude_capture\\integrations\\seamless_claude_integration.py --status
if "%choice%"=="3" python claude_capture\\tests\\claude_test_from_root.py
if "%choice%"=="4" call claude_capture\\setup\\install_dependencies.bat
if "%choice%"=="5" explorer claude_capture

pause
"""
    
    with open(root_dir / "claude_launcher.bat", 'w') as f:
        f.write(bat_launcher_content)
    
    print("✅ Created claude_launcher.sh")
    print("✅ Created claude_launcher.bat")
    
    # Update the main README in claude_capture
    readme_content = f"""# Claude Capture System - Organized Structure

## 📁 Folder Organization

```
claude_capture/
├── scripts/          # All executable management scripts
├── integrations/     # Python integration modules  
├── tests/           # Test files and verification scripts
├── setup/           # Installation and setup scripts
├── docs/            # Documentation and guides
└── README.md        # This file
```

## 🚀 Quick Start

### From Project Root:
```bash
# Windows
.\\claude_launcher.bat

# Linux/Mac
./claude_launcher.sh
```

### Direct Commands:
```bash
# Start capture
.\\claude_capture\\scripts\\claude_start.bat

# Check status
python claude_capture\\integrations\\seamless_claude_integration.py --status

# Run tests
python claude_capture\\tests\\claude_test_from_root.py

# Setup dependencies
.\\claude_capture\\setup\\install_dependencies.bat
```

## 📂 File Categories

### Scripts (`/scripts/`)
- `claude_capture_manager_fixed.ps1` - PowerShell manager (recommended)
- `claude_start.bat` - Simple start script
- `claude_quick_start.bat` - Guided setup
- `claude_capture_manager.sh` - Bash version
- `claude_capture_manager.bat` - Windows batch version

### Tests (`/tests/`)
- `claude_test_from_root.py` - Main test script (run from root)
- `test_claude_capture.py` - Alternative test script
- `test_capture_windows_fixed.py` - Windows-specific test
- `test_powershell.ps1` - PowerShell test

### Setup (`/setup/`)
- `install_dependencies.bat` - Install Python packages
- `setup_claude_capture.bat` - Complete setup script
- `requirements.txt` - Python dependencies

### Documentation (`/docs/`)
- `ZERO_COMMAND_SETUP.md` - Complete setup guide
- `CLAUDE_CODE_NEXT_LEVEL_INTEGRATION.md` - Advanced integration
- `CONTEXT_EVOLUTION_GUIDE.md` - Context system guide

## 🎯 Usage Examples

```bash
# Simplest start
.\\claude_launcher.bat

# Or direct PowerShell
.\\claude_capture\\scripts\\claude_capture_manager_fixed.ps1 start

# Or direct Python
python claude_capture\\integrations\\seamless_claude_integration.py --start
```

## 💾 Database Files (Root Directory)
- `claude_auto_capture.db` - Main conversation database
- `claude_session_state.json` - Session state tracking

*Last organized: {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(claude_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print("✅ Updated claude_capture/README.md")
    
    print("\n🎯 ORGANIZATION COMPLETE!")
    print("=" * 50)
    
    print("\n📋 SUMMARY:")
    print("✅ All Claude files organized into claude_capture/")
    print("✅ Scripts moved to claude_capture/scripts/")
    print("✅ Tests moved to claude_capture/tests/")
    print("✅ Setup files moved to claude_capture/setup/")
    print("✅ Documentation moved to claude_capture/docs/")
    print("✅ Quick launchers created in root")
    print("✅ Temporary files cleaned up")
    print("✅ README updated")
    
    print("\n🚀 READY TO USE:")
    print("• Quick start: .\\claude_launcher.bat")
    print("• PowerShell: .\\claude_capture\\scripts\\claude_capture_manager_fixed.ps1 start")
    print("• Direct: python claude_capture\\integrations\\seamless_claude_integration.py --start")
    
    return True

if __name__ == "__main__":
    print("🎯 Starting Claude Files Organization...")
    print("This will organize all Claude-related files into proper folders")
    print()
    
    try:
        success = organize_claude_files()
        if success:
            print("\n🎉 ORGANIZATION SUCCESSFUL!")
            print("All Claude files are now properly organized!")
        else:
            print("\n⚠️  ORGANIZATION FAILED")
            print("Please check the errors above")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Please check the error and try again")
    
    input("\nPress Enter to continue...")
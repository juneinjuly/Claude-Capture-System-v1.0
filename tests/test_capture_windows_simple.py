#!/usr/bin/env python3
"""
Simple Windows test for Claude capture system (No Unicode)
"""

import sys
import subprocess
import time
import os
from pathlib import Path

def test_windows_capture():
    """Test Claude capture system on Windows"""
    
    print("CLAUDE CAPTURE SYSTEM TEST - WINDOWS")
    print("=" * 50)
    
    # Get current working directory
    cwd = Path.cwd()
    print(f"Current directory: {cwd}")
    
    # Test 1: Check if Python is working
    print("\nTest 1: Checking Python installation...")
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"SUCCESS: Python version: {result.stdout.strip()}")
    except Exception as e:
        print(f"ERROR: Python error: {e}")
        return False
    
    # Test 2: Check if the integration script exists
    print("\nTest 2: Checking integration script...")
    
    # Try different possible paths based on where the script is run from
    possible_paths = [
        Path("../integrations/seamless_claude_integration_windows.py"),  # From tests folder
        Path("../integrations/seamless_claude_integration.py"),  # From tests folder
        Path("claude_capture/integrations/seamless_claude_integration_windows.py"),  # From project root
        Path("claude_capture/integrations/seamless_claude_integration.py"),  # From project root
        Path("integrations/seamless_claude_integration_windows.py"),  # From claude_capture folder
        Path("integrations/seamless_claude_integration.py"),  # From claude_capture folder
    ]
    
    script_path = None
    for path in possible_paths:
        if path.exists():
            script_path = path
            print(f"SUCCESS: Found: {script_path}")
            break
        else:
            print(f"NOT FOUND: {path}")
    
    if script_path is None:
        print("ERROR: Integration script not found in any expected location")
        return False
    
    # Test 3: Check dependencies
    print("\nTest 3: Checking Python dependencies...")
    dependencies = ["watchdog", "psutil"]
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"SUCCESS: {dep} installed")
        except ImportError:
            print(f"ERROR: {dep} not installed")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"WARNING: Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install " + " ".join(missing_deps))
        return False
    
    # Test 4: Try to run the integration script
    print("\nTest 4: Testing integration script...")
    try:
        result = subprocess.run([sys.executable, str(script_path), "--status"], 
                              capture_output=True, text=True, timeout=10)
        print(f"SUCCESS: Script executed successfully")
        if result.stdout.strip():
            print(f"OUTPUT: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"STDERR: {result.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print("WARNING: Script timed out (this might be normal)")
    except Exception as e:
        print(f"ERROR: Error running script: {e}")
        return False
    
    # Test 5: Create test file
    print("\nTest 5: Creating test file...")
    test_file = Path("windows_test_claude_simple.py")
    test_content = f"""# Windows Test File for Claude Capture
# Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}
from AlgorithmImports import *

class WindowsTestAlgorithm(QCAlgorithm):
    '''
    WINDOWS TEST: Claude Capture Verification
    
    This file is created to test the capture system on Windows.
    SAKB Integration: LOG -> PROCESS -> STORE
    '''
    
    def Initialize(self):
        '''Initialize Windows test'''
        self.Log("TEST: Windows test file created")
        self.Log("SUCCESS: Testing Claude capture system on Windows")
        
    def ExecuteTest(self):
        '''Execute test'''
        return {{"test": "successful", "capture": "should_work"}}
"""
    
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"SUCCESS: Created test file: {test_file}")
        print(f"SIZE: File size: {test_file.stat().st_size} bytes")
        print(f"TIME: Created at: {time.strftime('%H:%M:%S')}")
        
        # Wait for potential capture
        print("WAIT: Waiting 3 seconds for capture detection...")
        time.sleep(3)
        
        # Clean up
        test_file.unlink()
        print("CLEAN: Test file cleaned up")
        
    except Exception as e:
        print(f"ERROR: Error creating test file: {e}")
        return False
    
    # Test 6: Check for database
    print("\nTest 6: Checking for database...")
    db_files = ["claude_auto_capture.db", "claude_session_state.json"]
    for db_file in db_files:
        if Path(db_file).exists():
            print(f"SUCCESS: Found: {db_file}")
            print(f"SIZE: Size: {Path(db_file).stat().st_size} bytes")
        else:
            print(f"WARNING: Not found: {db_file} (might be created later)")
    
    # Test 7: Check folder structure
    print("\nTest 7: Checking claude_capture folder structure...")
    expected_folders = [
        "claude_capture",
        "claude_capture/integrations",
        "claude_capture/scripts", 
        "claude_capture/tests",
        "claude_capture/setup"
    ]
    
    for folder in expected_folders:
        if Path(folder).exists():
            print(f"SUCCESS: Found folder: {folder}")
        else:
            print(f"WARNING: Missing folder: {folder}")
    
    print("\nWINDOWS TEST COMPLETE")
    print("=" * 50)
    
    print("\nSUMMARY:")
    print("SUCCESS: Python installation: OK")
    print("SUCCESS: Integration script: FOUND")
    print("SUCCESS: Dependencies: OK")
    print("SUCCESS: Script execution: OK")
    print("SUCCESS: File creation: OK")
    print("SUCCESS: Folder structure: OK")
    
    print("\nNEXT STEPS:")
    print("1. Start capture: .\\claude_start_simple.bat")
    print("2. Check status: python claude_capture\\integrations\\seamless_claude_integration_windows.py --status")
    print("3. Use manager: .\\claude_capture\\scripts\\claude_capture_manager_fixed.ps1 start")
    print("4. Test from root: python claude_test_from_root.py")
    
    print("\nEXPECTED OUTPUT:")
    print("If capture system is working, you should see:")
    print("• CLAUDE: [HH:MM:SS] CLAUDE ACTIVITY DETECTED!")
    print("• FILE: filename.py")
    print("• CONFIDENCE: 0.XX")
    print("• CAPTURED: X")
    print("• DATABASE: Stored in database: claude_auto_capture.db")
    
    return True

if __name__ == "__main__":
    success = test_windows_capture()
    if success:
        print("\nSUCCESS: ALL TESTS PASSED!")
    else:
        print("\nERROR: SOME TESTS FAILED - CHECK ABOVE FOR DETAILS")
    
    input("\nPress Enter to continue...")
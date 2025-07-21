#!/usr/bin/env python3
"""
Windows-compatible test for Claude capture system
"""

import sys
import subprocess
import time
from pathlib import Path

def test_windows_capture():
    """Test Claude capture system on Windows"""
    
    print("🧪 CLAUDE CAPTURE SYSTEM TEST - WINDOWS")
    print("=" * 50)
    
    # Test 1: Check if Python is working
    print("🔧 Test 1: Checking Python installation...")
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python version: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python error: {e}")
        return False
    
    # Test 2: Check if the integration script exists
    print("\n🔧 Test 2: Checking integration script...")
    
    # Try different possible paths based on where the script is run from
    possible_paths = [
        Path("../integrations/seamless_claude_integration.py"),  # From tests folder
        Path("../../integrations/seamless_claude_integration.py"),  # From nested tests
        Path("claude_capture/integrations/seamless_claude_integration.py"),  # From project root
        Path("integrations/seamless_claude_integration.py"),  # From claude_capture folder
    ]
    
    script_path = None
    for path in possible_paths:
        if path.exists():
            script_path = path
            print(f"✅ Found: {script_path}")
            break
        else:
            print(f"❌ Not found: {path}")
    
    if script_path is None:
        print("❌ Integration script not found in any expected location")
        return False
    
    # Test 3: Try to run the integration script
    print("\n🔧 Test 3: Testing integration script...")
    try:
        result = subprocess.run([sys.executable, str(script_path), "--status"], 
                              capture_output=True, text=True, timeout=10)
        print(f"✅ Script output:")
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️  Script timed out (this might be normal)")
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False
    
    # Test 4: Check dependencies
    print("\n🔧 Test 4: Checking Python dependencies...")
    dependencies = ["watchdog", "psutil"]
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} installed")
        except ImportError:
            print(f"❌ {dep} not installed")
            print(f"   Install with: pip install {dep}")
    
    # Test 5: Create test file
    print("\n🔧 Test 5: Creating test file...")
    test_file = Path("windows_test_claude.py")
    test_content = """# 🤖 Windows Test File for Claude Capture
from AlgorithmImports import *

class WindowsTestAlgorithm(QCAlgorithm):
    \"\"\"
    WINDOWS TEST: Claude Capture Verification
    
    This file is created to test the capture system on Windows.
    SAKB Integration: LOG -> PROCESS -> STORE
    \"\"\"
    
    def Initialize(self):
        \"\"\"Initialize Windows test\"\"\"
        self.Log("🧪 Windows test file created")
        self.Log("✅ Testing Claude capture system on Windows")
"""
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    print(f"✅ Created: {test_file}")
    
    # Test 6: Try to start the capture system
    print("\n🔧 Test 6: Starting capture system...")
    try:
        # Start the process
        process = subprocess.Popen([sys.executable, "seamless_claude_integration.py", "--start"],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        print("✅ Capture system started")
        print("📱 Process ID:", process.pid)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Process is running")
            
            # Try to get some output
            try:
                stdout, stderr = process.communicate(timeout=5)
                if stdout:
                    print("📊 Output:")
                    print(stdout)
                if stderr:
                    print("⚠️  Errors:")
                    print(stderr)
            except subprocess.TimeoutExpired:
                print("⏰ Process still running (this is good)")
                process.terminate()
        else:
            print("❌ Process exited")
            stdout, stderr = process.communicate()
            if stdout:
                print("📊 Output:")
                print(stdout)
            if stderr:
                print("⚠️  Errors:")
                print(stderr)
        
    except Exception as e:
        print(f"❌ Error starting capture system: {e}")
        return False
    
    # Test 7: Check for database
    print("\n🔧 Test 7: Checking for database...")
    db_files = ["claude_auto_capture.db", "claude_session_state.json"]
    for db_file in db_files:
        if Path(db_file).exists():
            print(f"✅ Found: {db_file}")
        else:
            print(f"⚠️  Not found: {db_file} (might be created later)")
    
    # Clean up
    print("\n🧹 Cleaning up...")
    try:
        test_file.unlink()
        print(f"✅ Removed: {test_file}")
    except:
        pass
    
    print("\n🎯 WINDOWS TEST COMPLETE")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_windows_capture()
    input("\nPress Enter to continue...")
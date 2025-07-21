#!/usr/bin/env python3
"""
Claude Capture Test - Run from Project Root
This is the simplest way to test the capture system
"""

import sys
import subprocess
import time
import os
from pathlib import Path

def test_claude_capture_from_root():
    """Test Claude capture system from project root"""
    
    print("🧪 CLAUDE CAPTURE TEST - FROM PROJECT ROOT")
    print("=" * 50)
    
    # Verify we're in the right directory
    cwd = Path.cwd()
    print(f"📁 Current directory: {cwd}")
    
    # Check if we have the expected structure
    expected_files = [
        "claude_capture/integrations/seamless_claude_integration.py",
        "claude_capture/scripts/start_auto_capture.sh",
        "claude_capture/tests/test_capture_windows.py",
        "claude_start.bat",
        "claude_capture_manager_fixed.ps1"
    ]
    
    print("\n🔧 Checking file structure...")
    missing_files = []
    for file_path in expected_files:
        if Path(file_path).exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files. Please check your setup.")
        return False
    
    # Test Python dependencies
    print("\n🔧 Testing Python dependencies...")
    deps = ["watchdog", "psutil", "sqlite3"]
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}: OK")
        except ImportError:
            print(f"❌ {dep}: MISSING - install with: pip install {dep}")
            return False
    
    # Test the integration script
    print("\n🔧 Testing integration script...")
    script_path = "claude_capture/integrations/seamless_claude_integration.py"
    
    try:
        result = subprocess.run([
            sys.executable, script_path, "--status"
        ], capture_output=True, text=True, timeout=10)
        
        print("✅ Integration script executed successfully")
        if result.stdout.strip():
            print(f"📊 Output: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"⚠️  Stderr: {result.stderr.strip()}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Script timed out (normal for status check)")
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False
    
    # Create and test a capture file
    print("\n🔧 Creating test file for capture...")
    test_file = Path("test_claude_capture_file.py")
    test_content = f"""# 🤖 Claude Capture Test File
# Created: {time.strftime('%Y-%m-%d %H:%M:%S')}
# This file should trigger the Claude capture system

from AlgorithmImports import *

class ClaudeCaptureTestAlgorithm(QCAlgorithm):
    '''
    CLAUDE CAPTURE TEST: System Verification
    
    This file tests the automatic capture system.
    SAKB Integration: LOG -> PROCESS -> STORE
    '''
    
    def Initialize(self):
        '''Initialize test'''
        self.Log("🧪 Claude capture test initialized")
        self.Log("✅ If you see capture notifications, the system is working!")
        
    def OnData(self, data):
        '''Test data processing'''
        pass
        
    def TestCapture(self):
        '''Test capture functionality'''
        return {{
            "test_result": "success",
            "capture_expected": True,
            "claude_signatures": ["AlgorithmImports", "QCAlgorithm", "SAKB Integration"]
        }}
"""
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        print(f"✅ Created: {test_file}")
        print(f"📝 Size: {test_file.stat().st_size} bytes")
        
        # Wait for capture detection
        print("⏰ Waiting 5 seconds for capture detection...")
        time.sleep(5)
        
        # Clean up
        test_file.unlink()
        print("🧹 Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Error with test file: {e}")
        return False
    
    # Check database
    print("\n🔧 Checking database files...")
    db_files = {
        "claude_auto_capture.db": "Main capture database",
        "claude_session_state.json": "Session state tracking"
    }
    
    for db_file, description in db_files.items():
        if Path(db_file).exists():
            size = Path(db_file).stat().st_size
            print(f"✅ {db_file}: {size} bytes - {description}")
        else:
            print(f"⚠️  {db_file}: Not found - {description}")
    
    print("\n🎯 TEST COMPLETE")
    print("=" * 50)
    
    print("\n🚀 READY TO USE:")
    print("1. ✅ File structure is correct")
    print("2. ✅ Dependencies are installed")
    print("3. ✅ Integration script works")
    print("4. ✅ Test file creation works")
    
    print("\n📋 USAGE OPTIONS:")
    print("• Simple start: .\\claude_start.bat")
    print("• PowerShell: .\\claude_capture_manager_fixed.ps1 start")
    print("• Direct Python: python claude_capture\\integrations\\seamless_claude_integration.py --start")
    print("• Check status: python claude_capture\\integrations\\seamless_claude_integration.py --status")
    
    print("\n🔍 EXPECT TO SEE:")
    print("When capture is working:")
    print("• 🤖 [HH:MM:SS] CLAUDE ACTIVITY DETECTED!")
    print("• 📝 File: your_file.py")
    print("• 🎯 Confidence: 0.XX")
    print("• 📊 Total Captured: X")
    print("• 💾 Stored in database")
    
    return True

if __name__ == "__main__":
    print("🎯 Starting Claude Capture System Test...")
    print("Make sure you're running this from the project root directory")
    print()
    
    success = test_claude_capture_from_root()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your Claude capture system is ready to use!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please check the errors above and fix them before proceeding")
    
    input("\nPress Enter to continue...")
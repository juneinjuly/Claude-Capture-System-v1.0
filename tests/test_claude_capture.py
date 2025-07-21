#!/usr/bin/env python3
"""
Simple test for Claude capture system - Windows compatible
Run from project root directory
"""

import sys
import subprocess
import time
from pathlib import Path

def test_claude_capture():
    """Test Claude capture system"""
    
    print("🧪 CLAUDE CAPTURE SYSTEM TEST")
    print("=" * 40)
    
    # Test 1: Check Python
    print("🔧 Test 1: Checking Python...")
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python error: {e}")
        return False
    
    # Test 2: Check integration script
    print("\n🔧 Test 2: Checking integration script...")
    script_path = Path("claude_capture/integrations/seamless_claude_integration.py")
    if script_path.exists():
        print(f"✅ Found: {script_path}")
    else:
        print(f"❌ Not found: {script_path}")
        return False
    
    # Test 3: Check dependencies
    print("\n🔧 Test 3: Checking dependencies...")
    try:
        import watchdog
        print("✅ watchdog imported successfully")
    except ImportError:
        print("❌ watchdog not installed. Run: pip install watchdog")
        return False
    
    try:
        import psutil
        print("✅ psutil imported successfully")
    except ImportError:
        print("❌ psutil not installed. Run: pip install psutil")
        return False
    
    # Test 4: Test script status
    print("\n🔧 Test 4: Testing script status...")
    try:
        result = subprocess.run([sys.executable, str(script_path), "--status"], 
                              capture_output=True, text=True, timeout=10)
        print("✅ Script executed successfully")
        if result.stdout.strip():
            print(f"📊 Output: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"⚠️  Stderr: {result.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print("⚠️  Script timed out (might be normal)")
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False
    
    # Test 5: Create test file
    print("\n🔧 Test 5: Creating test file...")
    test_file = Path("test_claude_activity.py")
    test_content = f"""# 🤖 Test File for Claude Capture
# Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}

from AlgorithmImports import *

class TestClaudeActivityAlgorithm(QCAlgorithm):
    '''
    TEST: Claude Activity Detection Test
    
    This is a test file to verify the capture system is working.
    SAKB Integration: LOG -> PROCESS -> STORE
    '''
    
    def Initialize(self):
        '''Initialize test algorithm'''
        self.Log("🧪 Test algorithm initialized")
        self.Log("✅ If you see capture notifications, the system is working!")
"""
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_content)
        print(f"✅ Created test file: {test_file}")
        print(f"📝 File size: {test_file.stat().st_size} bytes")
        
        # Wait for potential capture
        print("⏰ Waiting 3 seconds for capture detection...")
        time.sleep(3)
        
        # Clean up
        test_file.unlink()
        print("🧹 Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Error creating test file: {e}")
        return False
    
    # Test 6: Check database
    print("\n🔧 Test 6: Checking database...")
    db_file = Path("claude_auto_capture.db")
    if db_file.exists():
        print(f"✅ Database exists: {db_file}")
        print(f"📊 Database size: {db_file.stat().st_size} bytes")
    else:
        print(f"⚠️  Database not found: {db_file} (may be created after first capture)")
    
    session_file = Path("claude_session_state.json")
    if session_file.exists():
        print(f"✅ Session file exists: {session_file}")
    else:
        print(f"⚠️  Session file not found: {session_file}")
    
    print("\n🎯 TEST COMPLETE")
    print("=" * 40)
    print("\n📋 WHAT TO EXPECT:")
    print("If the capture system is working, you should see:")
    print("• File modification notifications")
    print("• Claude signature analysis")
    print("• Activity detection messages")
    print("• Database entries created")
    print("\n🚀 NEXT STEPS:")
    print("1. Start capture: .\\claude_start.bat")
    print("2. Check status: python claude_capture\\integrations\\seamless_claude_integration.py --status")
    print("3. Create files and watch for capture notifications")
    
    return True

if __name__ == "__main__":
    test_claude_capture()
    input("\nPress Enter to continue...")
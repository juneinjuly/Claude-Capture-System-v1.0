#!/usr/bin/env python3
"""
Test script to verify Claude capture system is working
Creates test files that should trigger the capture system
"""

import os
import time
from pathlib import Path
from datetime import datetime

def create_test_claude_file():
    """Create a test file that should trigger Claude capture"""
    
    test_file = Path("test_claude_activity.py")
    
    # Create content that should trigger Claude detection
    content = f"""# region imports
from AlgorithmImports import *
import numpy as np
import pandas as pd
# endregion

class TestClaudeActivityAlgorithm(QCAlgorithm):
    \"\"\"
    TEST: Claude Activity Detection Test
    
    This is a test file to verify the Claude capture system is working.
    Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    SAKB Integration: LOG -> PROCESS -> STORE
    Strategic Question: "Is the Claude capture system working?"
    \"\"\"
    
    def Initialize(self):
        \"\"\"Initialize test algorithm\"\"\"
        
        self.SetStartDate(2024, 1, 1)
        self.SetEndDate(2024, 12, 31)
        self.SetCash(100000)
        
        # Test indicators
        self.rsi = RelativeStrengthIndex(14)
        
        self.Log("🤖 Test algorithm initialized")
        self.Log("✅ If you see capture notifications, the system is working!")
        
    def OnData(self, data):
        \"\"\"Test data processing\"\"\"
        pass
        
    def ExecuteTestAnalysis(self):
        \"\"\"Execute test analysis\"\"\"
        
        self.Log("📊 Executing test analysis...")
        self.Log("🎯 This should trigger Claude activity detection")
        
        # Test patterns that should be detected
        test_results = {{
            "claude_signatures": True,
            "implementation_code": True,
            "sakb_integration": True,
            "conversation_markers": True
        }}
        
        return test_results
"""
    
    # Write the test file
    with open(test_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Created test file: {test_file}")
    print(f"📝 File size: {test_file.stat().st_size} bytes")
    print(f"⏰ Created at: {datetime.now().strftime('%H:%M:%S')}")
    
    return test_file

def create_test_markdown_file():
    """Create a test markdown file that should trigger capture"""
    
    test_file = Path("test_claude_insights.md")
    
    content = f"""# 🤖 Claude Activity Test - Insights

## Test Purpose
This is a test file to verify the Claude capture system is working.

## Key Findings
- **Test File Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Strategic Implication**: If capture notifications appear, the system is working correctly
- **Important**: This file contains Claude signatures and should trigger detection

## SAKB Integration
- **LOG**: Raw test data captured
- **PROCESS**: Structured analysis of test results
- **STORE**: Strategic insights about system functionality

## Next Actions
1. Check console for capture notifications
2. Verify database entries
3. Confirm system is monitoring properly

## Test Results
🎯 **Expected Behavior**: You should see console output like:
```
🤖 [HH:MM:SS] CLAUDE ACTIVITY DETECTED!
   📝 File: test_claude_insights.md
   🎯 Confidence: 0.XX
   📊 Total Captured: X
   ✅ Claude signatures found
   ✅ Conversation markers found
   💾 Stored in database: claude_auto_capture.db
   ==================================================
```

If you see this output, the capture system is working perfectly! 🚀
"""
    
    with open(test_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Created test file: {test_file}")
    print(f"📝 File size: {test_file.stat().st_size} bytes")
    print(f"⏰ Created at: {datetime.now().strftime('%H:%M:%S')}")
    
    return test_file

def modify_existing_file():
    """Modify an existing file to trigger capture"""
    
    # Try to find an existing Python file to modify
    for file_path in Path(".").glob("*.py"):
        if file_path.name not in ["test_capture_system.py", "seamless_claude_integration.py"]:
            try:
                # Read existing content
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Add a Claude signature comment
                claude_comment = f"""
# 🤖 Claude Activity Test - Modified at {datetime.now().strftime('%H:%M:%S')}
# This modification should trigger the capture system
# SAKB Integration: Testing file modification detection
"""
                
                # Write back with the addition
                with open(file_path, 'w') as f:
                    f.write(claude_comment + content)
                
                print(f"✅ Modified existing file: {file_path}")
                print(f"📝 Added Claude signature comment")
                print(f"⏰ Modified at: {datetime.now().strftime('%H:%M:%S')}")
                
                return file_path
                
            except Exception as e:
                continue
    
    print("⚠️  No suitable existing file found to modify")
    return None

def run_capture_test():
    """Run the complete capture test"""
    
    print("🧪 CLAUDE CAPTURE SYSTEM TEST")
    print("=" * 50)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📝 Creating test files that should trigger capture...")
    print()
    
    # Create test files
    test_files = []
    
    # Test 1: Create Python file
    print("🔧 Test 1: Creating Claude-signature Python file...")
    py_file = create_test_claude_file()
    test_files.append(py_file)
    
    # Wait for file system to register
    time.sleep(1)
    
    # Test 2: Create Markdown file
    print()
    print("🔧 Test 2: Creating Claude-signature Markdown file...")
    md_file = create_test_markdown_file()
    test_files.append(md_file)
    
    # Wait for file system to register
    time.sleep(1)
    
    # Test 3: Modify existing file
    print()
    print("🔧 Test 3: Modifying existing file...")
    modified_file = modify_existing_file()
    if modified_file:
        test_files.append(modified_file)
    
    # Wait for processing
    time.sleep(2)
    
    print()
    print("🎯 TEST COMPLETE")
    print("=" * 50)
    print()
    print("🔍 WHAT TO LOOK FOR:")
    print("If the capture system is working, you should see output like:")
    print()
    print("🤖 [HH:MM:SS] CLAUDE ACTIVITY DETECTED!")
    print("   📝 File: test_claude_activity.py")
    print("   🎯 Confidence: 0.XX")
    print("   📊 Total Captured: X")
    print("   ✅ Claude signatures found")
    print("   ✅ Implementation code detected")
    print("   ✅ SAKB integration detected")
    print("   ✅ Conversation markers found")
    print("   💾 Stored in database: claude_auto_capture.db")
    print("   " + "="*50)
    print()
    print("📊 Check capture status with: ./check_capture_status.sh")
    print("🔍 Search captured data with: ./claude_session.sh search 'test'")
    print()
    print("🧹 Clean up test files with: rm test_claude_*")
    
    return test_files

if __name__ == "__main__":
    run_capture_test()
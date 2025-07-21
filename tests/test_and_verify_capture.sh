#!/bin/bash
# Test and verify Claude capture system with detailed logging

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_test() {
    echo -e "${PURPLE}[🧪]${NC} $1"
}

echo "🧪 CLAUDE CAPTURE SYSTEM - TEST & VERIFICATION"
echo "=" * 60

# Step 1: Check if capture system is running
print_info "Step 1: Checking if capture system is running..."
if pgrep -f "seamless_claude_integration.py" > /dev/null; then
    PID=$(pgrep -f "seamless_claude_integration.py")
    print_status "Capture system is running (PID: $PID)"
else
    print_warning "Capture system is not running"
    print_info "Starting capture system..."
    ./start_auto_capture.sh
    sleep 3
fi

echo ""

# Step 2: Run capture test
print_info "Step 2: Running capture test..."
print_test "Creating test files that should trigger capture..."
python3 test_capture_system.py

echo ""

# Step 3: Wait and check for capture activity
print_info "Step 3: Waiting for capture activity..."
print_info "Watching for capture notifications for 10 seconds..."
echo ""

# Monitor for capture activity
for i in {1..10}; do
    echo -ne "⏰ Waiting... $i/10\r"
    sleep 1
done

echo ""
echo ""

# Step 4: Check capture status
print_info "Step 4: Checking capture status..."
./check_capture_status.sh

echo ""

# Step 5: Check database
print_info "Step 5: Checking capture database..."
if [ -f "claude_auto_capture.db" ]; then
    print_status "Capture database exists"
    
    # Check database contents
    python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('claude_auto_capture.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM auto_conversations')
    conv_count = cursor.fetchone()[0]
    print(f'📊 Auto-conversations captured: {conv_count}')
    
    cursor.execute('SELECT COUNT(*) FROM activity_log')
    log_count = cursor.fetchone()[0]
    print(f'📊 Activity log entries: {log_count}')
    
    if conv_count > 0:
        print('✅ Capture system is working!')
        cursor.execute('SELECT timestamp, file_path FROM auto_conversations ORDER BY timestamp DESC LIMIT 3')
        recent = cursor.fetchall()
        print('📋 Recent captures:')
        for ts, fp in recent:
            print(f'   • {ts[:19]} - {fp}')
    else:
        print('⚠️  No conversations captured yet')
    
    conn.close()
except Exception as e:
    print(f'❌ Error checking database: {e}')
"
else
    print_warning "Capture database not found"
fi

echo ""

# Step 6: Show logs
print_info "Step 6: Checking recent logs..."
if [ -f "claude_session_state.json" ]; then
    print_status "Session state file exists"
    python3 -c "
import json
try:
    with open('claude_session_state.json', 'r') as f:
        data = json.load(f)
    print(f'📊 Session ID: {data.get(\"session_id\", \"N/A\")}')
    print(f'📊 Auto-session active: {data.get(\"auto_session_active\", False)}')
    print(f'📊 Conversations captured: {data.get(\"conversations_captured\", 0)}')
    print(f'📊 Last activity: {data.get(\"last_activity\", \"N/A\")}')
except Exception as e:
    print(f'❌ Error reading session state: {e}')
"
else
    print_warning "Session state file not found"
fi

echo ""

# Step 7: Test manual capture
print_info "Step 7: Testing manual capture..."
print_test "Creating additional test file..."

# Create a simple test file
cat > "manual_test_file.py" << 'EOF'
# 🤖 Manual Test File for Claude Capture
# This file should trigger the capture system

from AlgorithmImports import *

class ManualTestAlgorithm(QCAlgorithm):
    """
    MANUAL TEST: Claude Capture Verification
    
    This file is created to test the capture system manually.
    SAKB Integration: LOG -> PROCESS -> STORE
    """
    
    def Initialize(self):
        """Initialize manual test"""
        self.Log("🧪 Manual test file created")
        self.Log("✅ Testing Claude capture system")
        
    def ExecuteManualTest(self):
        """Execute manual test"""
        return {"test": "successful", "capture": "should_work"}
EOF

print_status "Created manual_test_file.py"
print_info "Waiting for capture detection..."
sleep 3

echo ""

# Step 8: Final verification
print_info "Step 8: Final verification..."
print_test "Checking if system detected our test files..."

python3 -c "
import sqlite3
import time
try:
    conn = sqlite3.connect('claude_auto_capture.db')
    cursor = conn.cursor()
    
    # Check for recent activity
    cursor.execute('SELECT COUNT(*) FROM auto_conversations WHERE timestamp > datetime(\"now\", \"-5 minutes\")')
    recent_count = cursor.fetchone()[0]
    
    if recent_count > 0:
        print('🎉 SUCCESS: Capture system is working!')
        print(f'📊 {recent_count} conversations captured in last 5 minutes')
        
        cursor.execute('SELECT timestamp, file_path, activity_detected FROM auto_conversations WHERE timestamp > datetime(\"now\", \"-5 minutes\")')
        recent = cursor.fetchall()
        
        print('📋 Recent capture activity:')
        for ts, fp, activity in recent:
            print(f'   • {ts[:19]} - {fp}')
    else:
        print('⚠️  No recent capture activity detected')
        print('💡 This might be normal if no Claude signatures were found')
    
    conn.close()
except Exception as e:
    print(f'❌ Error in final verification: {e}')
"

echo ""

# Step 9: Cleanup and summary
print_info "Step 9: Cleanup and summary..."
print_test "Cleaning up test files..."

# Remove test files
rm -f test_claude_*.py test_claude_*.md manual_test_file.py

echo ""
print_info "🎯 TEST COMPLETE"
echo "=" * 60
echo ""
print_info "📋 SUMMARY OF WHAT TO EXPECT:"
echo ""
print_info "✅ If capture system is working, you should have seen:"
echo "   • File modification notifications (👁️)"
echo "   • Claude signature analysis (🔍)"
echo "   • Activity detection messages (🤖)"
echo "   • Database entries created (📊)"
echo ""
print_info "🎛️  NEXT STEPS:"
echo "   • Use './ask.sh \"question\"' to test with real conversations"
echo "   • Monitor console for capture notifications"
echo "   • Check './claude_session.sh analytics' for captured data"
echo "   • Use './claude_session.sh search \"term\"' to find conversations"
echo ""
print_info "🔧 TROUBLESHOOTING:"
echo "   • If no captures: Check file permissions and Python dependencies"
echo "   • If errors: Check console output for specific error messages"
echo "   • If monitoring stops: Restart with './start_auto_capture.sh'"
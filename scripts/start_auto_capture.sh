#!/bin/bash
# Automatic Claude Code Integration - Zero-Command Setup
# This script starts seamless conversation capture that runs in the background

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

# Check if already running
if pgrep -f "seamless_claude_integration.py" > /dev/null; then
    print_info "Seamless Claude integration already running"
    python3 "$SCRIPT_DIR/../integrations/seamless_claude_integration.py" --status
    exit 0
fi

# Start the seamless integration
print_info "Starting seamless Claude Code integration..."
print_info "This will automatically capture all your conversations with Claude"
print_info "No manual commands needed - just use Claude normally!"

# Create a simple background process
nohup python3 "$SCRIPT_DIR/../integrations/seamless_claude_integration.py" --start > /dev/null 2>&1 &
INTEGRATION_PID=$!

# Wait a moment for startup
sleep 2

# Check if it started successfully
if kill -0 $INTEGRATION_PID 2>/dev/null; then
    print_success "Seamless Claude integration started successfully!"
    print_success "Process ID: $INTEGRATION_PID"
    
    # Save PID for later
    echo $INTEGRATION_PID > "$SCRIPT_DIR/claude_integration.pid"
    
    print_info "🤖 Auto-capture mode: ACTIVE"
    print_info "📱 All conversations will be automatically captured"
    print_info "👁️  File monitoring: ENABLED"
    print_info "📊 Use './claude_capture/scripts/check_capture_status.sh' to see activity"
    print_info "⏹️  Use './claude_capture/scripts/stop_auto_capture.sh' to stop"
    
    echo ""
    print_success "✨ You can now use Claude normally - everything is automatic!"
    print_success "💬 Just ask questions and the system captures everything"
    print_success "🔍 Search with: ./claude_capture/scripts/claude_session.sh search \"query\""
    print_success "📈 Analytics with: ./claude_capture/scripts/claude_session.sh analytics"
    
else
    print_warning "Failed to start seamless integration"
    exit 1
fi
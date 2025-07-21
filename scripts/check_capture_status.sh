#!/bin/bash
# Check status of automatic Claude Code integration

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

echo "🤖 Seamless Claude Integration Status Check"
echo "=" * 50

# Check if process is running
if pgrep -f "seamless_claude_integration.py" > /dev/null; then
    PID=$(pgrep -f "seamless_claude_integration.py")
    print_success "Auto-capture process running (PID: $PID)"
    
    # Get detailed status
    print_info "Getting detailed status..."
    python3 "$SCRIPT_DIR/../integrations/seamless_claude_integration.py" --status
    
    echo ""
    print_info "📊 Quick Analytics:"
    ./"$SCRIPT_DIR/claude_session.sh" analytics 2>/dev/null || echo "Analytics not available"
    
    echo ""
    print_info "🎯 Recent Activity:"
    # Show recent files modified
    find "$SCRIPT_DIR" -name "*.py" -o -name "*.md" -o -name "*.sh" | head -5 | while read file; do
        echo "  📝 $(basename "$file") - $(date -r "$file" "+%Y-%m-%d %H:%M:%S")"
    done
    
else
    print_warning "Auto-capture process not running"
    print_info "Start with: ./claude_capture/scripts/start_auto_capture.sh"
fi

echo ""
print_info "🎛️  Available Commands:"
echo "  • ./claude_capture/scripts/start_auto_capture.sh    - Start automatic capture"
echo "  • ./claude_capture/scripts/stop_auto_capture.sh     - Stop automatic capture"
echo "  • ./claude_capture/scripts/check_capture_status.sh  - Check status (this command)"
echo "  • ./claude_capture/scripts/claude_session.sh search \"query\" - Search conversations"
echo "  • ./claude_capture/scripts/claude_session.sh analytics - View analytics"
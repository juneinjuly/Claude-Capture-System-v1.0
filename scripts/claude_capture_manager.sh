#!/bin/bash
# Claude Capture Manager - Easy access to all Claude capture functionality

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLAUDE_CAPTURE_DIR="$SCRIPT_DIR/claude_capture"

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_claude() {
    echo -e "${PURPLE}[🤖]${NC} $1"
}

show_usage() {
    echo "🤖 Claude Capture Manager - Organized File Access"
    echo "=" * 60
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  start          - Start automatic capture"
    echo "  stop           - Stop automatic capture"
    echo "  status         - Check capture status"
    echo "  search <query> - Search captured conversations"
    echo "  analytics      - View analytics"
    echo "  test           - Run capture system test"
    echo "  list           - List all organized files"
    echo "  open           - Open claude_capture folder"
    echo ""
    echo "Examples:"
    echo "  $0 start                      # Start capture"
    echo "  $0 search \"RSI strategy\"       # Search conversations"
    echo "  $0 analytics                  # View analytics"
    echo "  $0 test                       # Test system"
    echo ""
}

list_files() {
    print_info "Claude Capture File Organization:"
    echo ""
    
    print_claude "📁 Scripts:"
    ls -la "$CLAUDE_CAPTURE_DIR/scripts/" | grep -E '\.(sh|bat)$' | awk '{print "   📜 " $9}'
    
    echo ""
    print_claude "📁 Integrations:"
    ls -la "$CLAUDE_CAPTURE_DIR/integrations/" | grep -E '\.py$' | awk '{print "   🐍 " $9}'
    
    echo ""
    print_claude "📁 Tests:"
    ls -la "$CLAUDE_CAPTURE_DIR/tests/" | grep -E '\.(py|sh)$' | awk '{print "   🧪 " $9}'
    
    echo ""
    print_claude "📁 Documentation:"
    ls -la "$CLAUDE_CAPTURE_DIR/docs/" | grep -E '\.md$' | awk '{print "   📖 " $9}'
}

open_folder() {
    print_info "Opening claude_capture folder..."
    
    # Try different methods to open folder
    if command -v nautilus &> /dev/null; then
        nautilus "$CLAUDE_CAPTURE_DIR" &
    elif command -v explorer &> /dev/null; then
        explorer "$CLAUDE_CAPTURE_DIR" &
    elif command -v open &> /dev/null; then
        open "$CLAUDE_CAPTURE_DIR" &
    else
        print_warning "Could not auto-open folder. Path: $CLAUDE_CAPTURE_DIR"
    fi
}

# Main script logic
case "$1" in
    "start")
        print_info "Starting Claude capture system..."
        "$CLAUDE_CAPTURE_DIR/scripts/start_auto_capture.sh"
        ;;
    "stop")
        print_info "Stopping Claude capture system..."
        "$CLAUDE_CAPTURE_DIR/scripts/stop_auto_capture.sh"
        ;;
    "status")
        print_info "Checking capture status..."
        "$CLAUDE_CAPTURE_DIR/scripts/check_capture_status.sh"
        ;;
    "search")
        if [ -z "$2" ]; then
            print_warning "Please provide a search query"
            echo "Usage: $0 search \"your query\""
            exit 1
        fi
        "$CLAUDE_CAPTURE_DIR/scripts/claude_session.sh" search "$2"
        ;;
    "analytics")
        print_info "Viewing analytics..."
        "$CLAUDE_CAPTURE_DIR/scripts/claude_session.sh" analytics
        ;;
    "test")
        print_info "Running capture system test..."
        "$CLAUDE_CAPTURE_DIR/tests/test_and_verify_capture.sh"
        ;;
    "list")
        list_files
        ;;
    "open")
        open_folder
        ;;
    *)
        show_usage
        ;;
esac
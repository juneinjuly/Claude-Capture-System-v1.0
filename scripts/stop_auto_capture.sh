#!/bin/bash
# Stop automatic Claude Code integration

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info "Stopping seamless Claude integration..."

# Try to stop using PID file
PID_FILE="$SCRIPT_DIR/claude_integration.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        print_success "Stopped integration process (PID: $PID)"
    else
        print_info "Process $PID not running"
    fi
    rm "$PID_FILE"
fi

# Also kill any remaining processes
pkill -f "seamless_claude_integration.py"

# Run cleanup
python3 "$SCRIPT_DIR/../integrations/seamless_claude_integration.py" --integrate

print_success "Seamless Claude integration stopped"
print_info "📊 Final integration completed"
print_info "🔍 Use './claude_capture/scripts/claude_session.sh analytics' to see captured data"
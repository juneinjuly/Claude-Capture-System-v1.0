#!/bin/bash
# Enhanced ask.sh with seamless auto-capture integration
# Use this instead of the original ask.sh for automatic conversation capture

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if question is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"your question\""
    echo "Example: $0 \"Based on Test #4 results, how should we approach Test #5?\""
    exit 1
fi

# Path to comprehensive context file
CONTEXT_FILE="$SCRIPT_DIR/COMPREHENSIVE_CONTEXT.md"

# Check if context file exists
if [ ! -f "$CONTEXT_FILE" ]; then
    echo "Error: COMPREHENSIVE_CONTEXT.md file not found in $SCRIPT_DIR"
    exit 1
fi

# Check if auto-capture is running
AUTO_CAPTURE_RUNNING=false
if pgrep -f "seamless_claude_integration.py" > /dev/null; then
    AUTO_CAPTURE_RUNNING=true
fi

# Display what we're doing
echo -e "${PURPLE}[🤖]${NC} Asking Claude with full context..."
if [ "$AUTO_CAPTURE_RUNNING" = true ]; then
    echo -e "${GREEN}[✓]${NC} Auto-capture active - conversation will be automatically saved"
else
    echo -e "${BLUE}[ℹ]${NC} Auto-capture not running - use ./start_auto_capture.sh to enable"
fi

echo -e "${BLUE}[ℹ]${NC} Question: $*"
echo -e "${BLUE}[ℹ]${NC} Context loaded from: $CONTEXT_FILE"
echo ""

# Store the question for potential capture
USER_QUESTION="$*"

# Run the context-aware query
echo "=== CONTEXT-AWARE AI QUERY ==="
cat "$CONTEXT_FILE"
echo ""
echo "USER QUESTION: $USER_QUESTION"
echo ""
echo "Please provide a comprehensive response that takes into account the full project context above."

# If auto-capture is running, the seamless system will detect this activity
# and automatically capture the conversation through file monitoring

# If auto-capture is not running, offer to start it
if [ "$AUTO_CAPTURE_RUNNING" = false ]; then
    echo ""
    echo -e "${BLUE}[ℹ]${NC} 💡 Tip: Start auto-capture to automatically save all conversations:"
    echo "    ./start_auto_capture.sh"
    echo ""
    echo -e "${BLUE}[ℹ]${NC} 🔍 Or manually capture this conversation:"
    echo "    ./claude_session.sh capture"
fi
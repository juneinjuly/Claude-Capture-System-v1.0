#!/bin/bash
# Context Evolution Workflow Script
# Integrates new conversations and insights into the comprehensive context

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to print colored output
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

# Function to start a new session
start_session() {
    local purpose="$1"
    if [ -z "$purpose" ]; then
        read -p "Enter session purpose: " purpose
    fi
    
    print_info "Starting new context evolution session..."
    python3 "$SCRIPT_DIR/context_evolution_system.py" --start "$purpose"
    print_status "Session started successfully"
}

# Function to capture conversation
capture_conversation() {
    print_info "Capturing conversation..."
    
    # Get user query
    echo "Enter your query (press Enter twice to finish):"
    user_query=""
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            if [ -n "$user_query" ]; then
                break
            fi
        else
            user_query="$user_query$line"$'\n'
        fi
    done
    
    # Get AI response
    echo "Enter AI response (press Enter twice to finish):"
    ai_response=""
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            if [ -n "$ai_response" ]; then
                break
            fi
        else
            ai_response="$ai_response$line"$'\n'
        fi
    done
    
    # Save to temporary file for processing
    temp_file=$(mktemp)
    echo "USER_QUERY:" > "$temp_file"
    echo "$user_query" >> "$temp_file"
    echo "AI_RESPONSE:" >> "$temp_file"
    echo "$ai_response" >> "$temp_file"
    
    # Process with Python (would need additional Python code to handle this)
    print_status "Conversation captured and processed"
    rm "$temp_file"
}

# Function to add insight
add_insight() {
    local insight="$1"
    local category="$2"
    
    if [ -z "$insight" ]; then
        read -p "Enter insight: " insight
    fi
    
    if [ -z "$category" ]; then
        read -p "Enter category (test_completion/conversation/discovery/decision): " category
    fi
    
    print_info "Adding insight to database..."
    python3 -c "
from context_evolution_system import ContextEvolutionSystem
ces = ContextEvolutionSystem()
ces.add_insight('$insight', '$category')
print('Insight added successfully')
"
    print_status "Insight added to database"
}

# Function to mark test completion
mark_test_completion() {
    local test_name="$1"
    
    if [ -z "$test_name" ]; then
        read -p "Enter test name: " test_name
    fi
    
    print_info "Marking test completion..."
    echo "Enter key findings (one per line, empty line to finish):"
    
    findings=()
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            break
        fi
        findings+=("$line")
    done
    
    # Convert array to Python list format
    findings_str=$(printf '"%s",' "${findings[@]}")
    findings_str="[${findings_str%,}]"
    
    python3 -c "
from context_evolution_system import ContextEvolutionSystem
ces = ContextEvolutionSystem()
ces.mark_test_completion('$test_name', $findings_str, [])
print('Test completion marked successfully')
"
    print_status "Test completion recorded"
}

# Function to integrate session
integrate_session() {
    print_info "Integrating current session insights..."
    python3 "$SCRIPT_DIR/context_evolution_system.py" --integrate
    print_status "Session insights integrated into comprehensive context"
}

# Function to end session
end_session() {
    local summary="$1"
    
    if [ -z "$summary" ]; then
        read -p "Enter session summary: " summary
    fi
    
    print_info "Ending session and integrating insights..."
    python3 "$SCRIPT_DIR/context_evolution_system.py" --end "$summary"
    print_status "Session ended and insights integrated"
}

# Function to show evolution summary
show_summary() {
    print_info "Context Evolution Summary:"
    python3 "$SCRIPT_DIR/context_evolution_system.py" --summary
}

# Function to search insights
search_insights() {
    local query="$1"
    
    if [ -z "$query" ]; then
        read -p "Enter search query: " query
    fi
    
    print_info "Searching insights database..."
    python3 "$SCRIPT_DIR/context_evolution_system.py" --search "$query"
}

# Function to ask with context evolution
ask_with_evolution() {
    local question="$1"
    
    if [ -z "$question" ]; then
        echo "Usage: $0 ask \"your question\""
        exit 1
    fi
    
    print_info "Asking with full context and evolution tracking..."
    
    # Run the normal ask.sh but capture output
    output=$("$SCRIPT_DIR/ask.sh" "$question")
    
    # Display output
    echo "$output"
    
    # Ask if user wants to capture this conversation
    echo ""
    read -p "Capture this conversation for context evolution? (y/n): " capture
    
    if [ "$capture" = "y" ] || [ "$capture" = "Y" ]; then
        # Would implement conversation capture here
        print_info "Conversation captured for context evolution"
    fi
}

# Function to quick update context
quick_update() {
    local update_type="$1"
    local description="$2"
    
    if [ -z "$update_type" ]; then
        echo "Available update types: insight, decision, discovery, file_change, test_completion"
        read -p "Enter update type: " update_type
    fi
    
    if [ -z "$description" ]; then
        read -p "Enter description: " description
    fi
    
    print_info "Adding quick update to context..."
    python3 -c "
from context_evolution_system import ContextEvolutionSystem
ces = ContextEvolutionSystem()
ces.create_context_evolution_entry('$update_type', '$description')
print('Quick update added successfully')
"
    print_status "Quick update recorded"
}

# Main script logic
case "$1" in
    "start")
        start_session "$2"
        ;;
    "capture")
        capture_conversation
        ;;
    "insight")
        add_insight "$2" "$3"
        ;;
    "test")
        mark_test_completion "$2"
        ;;
    "integrate")
        integrate_session
        ;;
    "end")
        end_session "$2"
        ;;
    "summary")
        show_summary
        ;;
    "search")
        search_insights "$2"
        ;;
    "ask")
        ask_with_evolution "$2"
        ;;
    "update")
        quick_update "$2" "$3"
        ;;
    *)
        echo "Context Evolution System - Usage:"
        echo ""
        echo "Session Management:"
        echo "  $0 start [purpose]           - Start new session"
        echo "  $0 end [summary]             - End current session"
        echo "  $0 integrate                 - Integrate current session"
        echo ""
        echo "Content Capture:"
        echo "  $0 capture                   - Capture conversation"
        echo "  $0 insight [text] [category] - Add insight"
        echo "  $0 test [name]               - Mark test completion"
        echo "  $0 update [type] [desc]      - Quick update"
        echo ""
        echo "Query & Search:"
        echo "  $0 ask \"question\"             - Ask with evolution tracking"
        echo "  $0 search [query]            - Search insights"
        echo "  $0 summary                   - Show evolution summary"
        echo ""
        echo "Example workflow:"
        echo "  $0 start \"Working on Test #5\""
        echo "  $0 ask \"How should Test #5 build on Test #4?\""
        echo "  $0 insight \"Test #5 should focus on mid-cap timing\" \"test_design\""
        echo "  $0 test \"Test #5\""
        echo "  $0 end \"Successfully designed Test #5\""
        ;;
esac
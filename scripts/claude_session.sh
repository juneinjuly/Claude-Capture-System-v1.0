#!/bin/bash
# Claude Code Integration Session Manager
# Automatically captures and integrates Claude Code conversations

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_claude() {
    echo -e "${PURPLE}[🤖]${NC} $1"
}

# Function to start Claude session
start_claude_session() {
    local purpose="$1"
    if [ -z "$purpose" ]; then
        read -p "Enter session purpose: " purpose
    fi
    
    print_info "Starting Claude Code integration session..."
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --start "$purpose"
    print_status "Claude session started with monitoring"
}

# Function to ask with Claude integration
ask_claude() {
    local question="$1"
    
    if [ -z "$question" ]; then
        echo "Usage: $0 ask \"your question\""
        exit 1
    fi
    
    print_info "Asking Claude with full context and conversation capture..."
    
    # Run the normal ask.sh and capture output
    output=$("$SCRIPT_DIR/ask.sh" "$question")
    
    # Display output
    echo "$output"
    
    # Extract user input and Claude response for integration
    user_input="$question"
    claude_response="$output"
    
    # Auto-capture the conversation
    print_info "Auto-capturing conversation for integration..."
    
    # Create temporary files for the conversation
    user_file=$(mktemp)
    claude_file=$(mktemp)
    
    echo "$user_input" > "$user_file"
    echo "$claude_response" > "$claude_file"
    
    # Capture with Python system
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --capture "$user_input" "$claude_response"
    
    # Clean up
    rm "$user_file" "$claude_file"
    
    print_status "Conversation captured and analyzed"
}

# Function to manually capture conversation
capture_conversation() {
    print_info "Manual conversation capture..."
    
    echo "Enter your question/input (press Enter twice to finish):"
    user_input=""
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            if [ -n "$user_input" ]; then
                break
            fi
        else
            user_input="$user_input$line"$'\n'
        fi
    done
    
    echo "Enter Claude's response (press Enter twice to finish):"
    claude_response=""
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            if [ -n "$claude_response" ]; then
                break
            fi
        else
            claude_response="$claude_response$line"$'\n'
        fi
    done
    
    # Capture with Python system
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --capture "$user_input" "$claude_response"
    
    print_status "Conversation captured and analyzed"
}

# Function to add quick insight
add_insight() {
    local insight="$1"
    
    if [ -z "$insight" ]; then
        read -p "Enter insight: " insight
    fi
    
    print_info "Adding insight to Claude session..."
    
    # Use the existing evolution system
    python3 -c "
try:
    from claude_code_integration import ClaudeCodeIntegrationSystem
    ccis = ClaudeCodeIntegrationSystem()
    if ccis.evolution_system:
        ccis.evolution_system.add_insight('$insight', 'claude_session')
        print('✓ Insight added successfully')
    else:
        print('⚠ Evolution system not available')
except Exception as e:
    print(f'✗ Error: {e}')
"
}

# Function to mark test completion
mark_test_completion() {
    local test_name="$1"
    
    if [ -z "$test_name" ]; then
        read -p "Enter test name: " test_name
    fi
    
    print_info "Marking test completion in Claude session..."
    
    echo "Enter key findings (one per line, empty line to finish):"
    findings=()
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            break
        fi
        findings+=("$line")
    done
    
    # Mark completion
    python3 -c "
try:
    from claude_code_integration import ClaudeCodeIntegrationSystem
    ccis = ClaudeCodeIntegrationSystem()
    if ccis.evolution_system:
        findings_list = [$(printf '"%s",' "${findings[@]}" | sed 's/,$//')]
        ccis.evolution_system.mark_test_completion('$test_name', findings_list, [])
        print('✓ Test completion marked')
    else:
        print('⚠ Evolution system not available')
except Exception as e:
    print(f'✗ Error: {e}')
"
}

# Function to search conversations
search_conversations() {
    local query="$1"
    
    if [ -z "$query" ]; then
        read -p "Enter search query: " query
    fi
    
    print_info "Searching Claude conversations..."
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --search "$query"
}

# Function to get session summary
get_session_summary() {
    local session_id="$1"
    
    if [ -z "$session_id" ]; then
        session_id="current"
    fi
    
    print_info "Getting Claude session summary..."
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --summary "$session_id"
}

# Function to end Claude session
end_claude_session() {
    local summary="$1"
    
    if [ -z "$summary" ]; then
        read -p "Enter session summary: " summary
    fi
    
    print_info "Ending Claude session and integrating insights..."
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --end "$summary"
    print_status "Claude session ended and context updated"
}

# Function to show conversation analytics
show_analytics() {
    print_info "Claude Code Conversation Analytics:"
    
    # Get database stats
    python3 -c "
try:
    import sqlite3
    from pathlib import Path
    
    db_path = Path('claude_conversations.db')
    if not db_path.exists():
        print('No conversation database found')
        exit()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Overall stats
    cursor.execute('SELECT COUNT(*) FROM conversations')
    total_conversations = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM sessions')
    total_sessions = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(importance_score) FROM conversations')
    avg_importance = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM conversations WHERE code_generated = 1')
    code_conversations = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM conversations WHERE context_impact = \"critical\"')
    critical_conversations = cursor.fetchone()[0]
    
    print(f'📊 Total Conversations: {total_conversations}')
    print(f'📊 Total Sessions: {total_sessions}')
    print(f'📊 Average Importance Score: {avg_importance:.2f}')
    print(f'📊 Code Generation Conversations: {code_conversations}')
    print(f'📊 Critical Impact Conversations: {critical_conversations}')
    
    # Recent activity
    cursor.execute('SELECT COUNT(*) FROM conversations WHERE date(timestamp) = date(\"now\")')
    today_conversations = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM conversations WHERE date(timestamp) >= date(\"now\", \"-7 days\")')
    week_conversations = cursor.fetchone()[0]
    
    print(f'📊 Today: {today_conversations} conversations')
    print(f'📊 This Week: {week_conversations} conversations')
    
    conn.close()
except Exception as e:
    print(f'Error getting analytics: {e}')
"
}

# Function to export conversation data
export_conversations() {
    local format="$1"
    
    if [ -z "$format" ]; then
        format="json"
    fi
    
    print_info "Exporting conversations in $format format..."
    
    # Export with Python
    python3 -c "
try:
    import sqlite3
    import json
    import csv
    from pathlib import Path
    from datetime import datetime
    
    db_path = Path('claude_conversations.db')
    if not db_path.exists():
        print('No conversation database found')
        exit()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM conversations ORDER BY timestamp DESC')
    conversations = cursor.fetchall()
    
    columns = [description[0] for description in cursor.description]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if '$format' == 'json':
        output_file = f'claude_conversations_export_{timestamp}.json'
        data = [dict(zip(columns, row)) for row in conversations]
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f'✓ Exported {len(conversations)} conversations to {output_file}')
    
    elif '$format' == 'csv':
        output_file = f'claude_conversations_export_{timestamp}.csv'
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(conversations)
        print(f'✓ Exported {len(conversations)} conversations to {output_file}')
    
    conn.close()
except Exception as e:
    print(f'Error exporting: {e}')
"
}

# Function to start auto-monitoring
start_monitoring() {
    print_info "Starting Claude Code auto-monitoring..."
    print_warning "This will monitor file changes and capture Claude activity"
    print_warning "Press Ctrl+C to stop monitoring"
    
    python3 "$SCRIPT_DIR/../integrations/claude_code_integration.py" --monitor
}

# Function to quick demo
demo_claude_integration() {
    print_claude "🚀 Claude Code Integration Demo"
    echo ""
    
    print_info "1. Starting demo session..."
    start_claude_session "Claude Integration Demo"
    
    sleep 2
    
    print_info "2. Asking a question with auto-capture..."
    ask_claude "What are the key benefits of the Claude Code Integration System?"
    
    sleep 2
    
    print_info "3. Adding a manual insight..."
    add_insight "The Claude integration system provides automatic conversation capture and analysis"
    
    sleep 2
    
    print_info "4. Getting session summary..."
    get_session_summary "current"
    
    sleep 2
    
    print_info "5. Ending demo session..."
    end_claude_session "Completed Claude integration demo successfully"
    
    print_status "Demo completed! Check the generated files and database."
}

# Main script logic
case "$1" in
    "start")
        start_claude_session "$2"
        ;;
    "ask")
        ask_claude "$2"
        ;;
    "capture")
        capture_conversation
        ;;
    "insight")
        add_insight "$2"
        ;;
    "test")
        mark_test_completion "$2"
        ;;
    "search")
        search_conversations "$2"
        ;;
    "summary")
        get_session_summary "$2"
        ;;
    "end")
        end_claude_session "$2"
        ;;
    "analytics")
        show_analytics
        ;;
    "export")
        export_conversations "$2"
        ;;
    "monitor")
        start_monitoring
        ;;
    "demo")
        demo_claude_integration
        ;;
    *)
        echo "🤖 Claude Code Integration System - Usage:"
        echo ""
        echo "Session Management:"
        echo "  $0 start [purpose]           - Start Claude session with monitoring"
        echo "  $0 end [summary]             - End Claude session and integrate"
        echo ""
        echo "Conversation Capture:"
        echo "  $0 ask \"question\"             - Ask with auto-capture"
        echo "  $0 capture                   - Manual conversation capture"
        echo "  $0 insight [text]            - Add insight to session"
        echo "  $0 test [name]               - Mark test completion"
        echo ""
        echo "Analysis & Search:"
        echo "  $0 search [query]            - Search conversations"
        echo "  $0 summary [session_id]      - Get session summary"
        echo "  $0 analytics                 - Show conversation analytics"
        echo "  $0 export [json|csv]         - Export conversation data"
        echo ""
        echo "Advanced Features:"
        echo "  $0 monitor                   - Start auto-monitoring"
        echo "  $0 demo                      - Run integration demo"
        echo ""
        echo "🔥 Next-Level Workflow:"
        echo "  $0 start \"Working on Test #5\""
        echo "  $0 ask \"How should Test #5 build on Test #4?\""
        echo "  $0 insight \"Test #5 should focus on mid-cap timing\""
        echo "  $0 test \"Test #5\""
        echo "  $0 end \"Test #5 design complete\""
        echo "  $0 analytics"
        echo ""
        echo "🎯 Key Features:"
        echo "  • Automatic conversation capture and analysis"
        echo "  • Intelligent insight extraction"
        echo "  • Real-time file monitoring"
        echo "  • Searchable conversation database"
        echo "  • Integration with comprehensive context"
        echo "  • Session-based organization"
        echo "  • Conversation analytics and export"
        ;;
esac
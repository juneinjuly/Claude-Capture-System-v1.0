# 📖 Claude Capture System - Comprehensive Usage Guide

## 🎯 Table of Contents
1. [Quick Start](#quick-start)
2. [System Overview](#system-overview)
3. [Basic Usage](#basic-usage)
4. [Enterprise Features](#enterprise-features)
5. [Team Collaboration](#team-collaboration)
6. [Advanced Queries](#advanced-queries)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## 🚀 Quick Start

### Immediate Actions:
```powershell
# Test everything works
.\claude test

# Start capturing conversations
.\claude start

# Check system status
.\claude status

# Get help
.\claude help
```

## 🏗️ System Overview

### What This System Does:
- **Captures** every Claude conversation automatically
- **Analyzes** conversations for insights, decisions, and action items
- **Organizes** information into a searchable knowledge graph
- **Enables** team collaboration and knowledge sharing
- **Provides** enterprise-grade analytics and reporting

### Architecture:
```
🧠 Intelligence Layer    - Knowledge graph with Neo4j
👥 Collaboration Layer  - Multi-user team framework  
💾 Data Layer          - SQLite databases with auto-capture
🎮 Interface Layer     - Simple commands and enterprise tools
```

## 📋 Basic Usage

### 1. Starting the System
```powershell
# From project root
.\claude start

# You'll see confirmation:
# "CLAUDE: Seamless Claude integration active"
# "STATUS: Auto-capture mode: ON"
```

### 2. Normal Claude Usage
- **Just talk to Claude normally!**
- The system automatically detects and captures:
  - All conversations
  - File modifications
  - Code generation
  - Decision points
  - Insights and learnings

### 3. Monitoring Activity
```powershell
# Check if capture is working
.\claude status

# Look for messages like:
# "CLAUDE ACTIVITY DETECTED!"
# "Conversation captured and analyzed"
```

### 4. Basic Queries
Ask Claude things like:
- "What did we work on yesterday?"
- "Show me our recent decisions"
- "What files have we modified?"
- "What insights have we discovered?"

## 🏢 Enterprise Features

### Knowledge Graph Engine
The system builds an intelligent graph of:
- **Insights** - Key learnings and discoveries
- **Decisions** - Choices made and their rationale
- **Action Items** - TODOs and next steps
- **Files** - Code and documents worked on
- **Sessions** - Conversation groupings
- **Relationships** - How everything connects

### Starting Enterprise Mode:
```powershell
# Launch enterprise features
.\claude_capture\enterprise_launch.bat

# Or directly:
python claude_capture\integrations\enterprise_intelligence_system.py
```

### Enterprise Queries:
```python
# Initialize enterprise system
from claude_capture.integrations.enterprise_intelligence_system import EnterpriseIntelligenceSystem
eis = EnterpriseIntelligenceSystem()

# Decision traceability
trace = eis.execute_decision_trace_query("60-day lookback period")
# Shows: What insights led to this decision + what files were affected

# Unified search
results = eis.search_across_systems("optimization strategy")
# Searches both conversations and knowledge graph

# Team analytics
report = eis.generate_team_intelligence_report("Engineering", "week")
# Shows: Team activity, decision velocity, insight generation
```

## 👥 Team Collaboration

### User Roles:
- **ADMIN** - Full system access
- **SENIOR_PM** - Project management capabilities
- **RESEARCHER** - Research channel access
- **DEVELOPER** - Development channel access
- **ANALYST** - Analytics and reporting
- **VIEWER** - Read-only access

### Channel Types:
- **#project-** - Project-specific discussions
- **#research-** - Research and discovery
- **#infrastructure-** - Infrastructure and DevOps
- **#strategy-** - Strategic planning
- **#general-** - Team announcements

### Setting Up Team Mode:
```python
# Create users
from claude_capture.integrations.multi_agent_collaboration import MultiAgentCollaborationFramework, UserRole

mcf = MultiAgentCollaborationFramework()

# Add team members
admin_id = mcf.create_user("admin", "System Admin", "admin@company.com", UserRole.ADMIN, "Platform")
dev_id = mcf.create_user("alice", "Alice Smith", "alice@company.com", UserRole.DEVELOPER, "Engineering")

# Create channels
mcf.create_default_channels(admin_id)

# Add users to channels
mcf.join_channel(dev_id, project_channel_id)
```

## 🔍 Advanced Queries

### Decision Traceability:
```python
# "Show me everything that led to using 60-day lookback"
trace = eis.execute_decision_trace_query("60-day lookback")

# Returns:
# - The decision itself
# - All insights that influenced it
# - Files that were modified as a result
# - Team discussions that led to it
```

### Pattern Discovery:
```python
# Search for patterns
results = eis.search_across_systems("performance optimization")

# Find related insights
related = eis.knowledge_graph.get_insight_network(insight_id)
```

### Team Analytics:
```python
# Weekly team report
report = eis.generate_team_intelligence_report("Engineering", "week")

# Includes:
# - Most active contributors
# - Decision velocity (decisions per day)
# - Insight generation rate
# - Channel activity patterns
```

### Real-time Dashboard:
```python
# Get live dashboard data
dashboard = eis.create_intelligence_dashboard_data()

# Shows:
# - Active users in last hour
# - Recent activity stream
# - Team leaderboard
# - System health status
```

## 🛠️ Troubleshooting

### Common Issues:

#### "No Claude signatures detected"
- **Cause**: System is monitoring but not finding Claude activity
- **Solution**: This is normal for system files. Work on actual code with Claude to see captures.

#### "System not starting"
- **Cause**: Missing dependencies or permissions
- **Solution**: 
  ```powershell
  # Reinstall dependencies
  .\claude_capture\setup\install_dependencies.bat
  
  # Run as administrator if needed
  ```

#### "Database not found"
- **Cause**: Database files not in correct location
- **Solution**: Check `claude_capture/data/` folder for database files

#### "Enterprise features not working"
- **Cause**: Missing Python packages
- **Solution**:
  ```powershell
  # Install all dependencies
  pip install sqlite3 neo4j watchdog psutil
  ```

### Debug Mode:
```powershell
# Run with verbose output
python claude_capture\integrations\seamless_claude_integration_windows.py --debug

# Check test results
.\claude_capture\tests\test_enterprise_system.py
```

## 📚 Best Practices

### For Individuals:
1. **Start Simple**: Use `.\claude start` and just talk to Claude normally
2. **Check Status**: Run `.\claude status` periodically to ensure capture is working
3. **Use Specific Terms**: Say "DECISION:", "INSIGHT:", "TODO:" to help the system categorize
4. **Ask for Summaries**: Regularly ask Claude to summarize your work

### For Teams:
1. **Set Up Channels**: Organize work by project/topic using appropriate channels
2. **Use Consistent Naming**: Follow the channel prefix conventions (#project-, #research-)
3. **Regular Reports**: Generate weekly team intelligence reports
4. **Share Insights**: Use the search function to avoid duplicate work

### For Search:
1. **Be Specific**: Instead of "that thing", search for "60-day lookback optimization"
2. **Use Keywords**: Include key terms like file names, algorithm names, etc.
3. **Try Different Queries**: Search for concepts, not just exact phrases
4. **Use Decision Traces**: When you want to understand "why", use decision traceability

### For Long-term Success:
1. **Consistent Usage**: The more you use it, the smarter it gets
2. **Team Training**: Make sure everyone knows the basic commands
3. **Regular Cleanup**: Occasionally review and organize older conversations
4. **Feedback Loop**: Use analytics to understand team patterns and improve workflows

## 🎯 Advanced Tips

### Smart Conversation Patterns:
```
✅ Good: "INSIGHT: The optimization approach provides better performance"
✅ Good: "DECISION: We'll implement the new risk calculation method"
✅ Good: "TODO: Update the backtest with new parameters"
```

### Effective Searching:
```python
# Instead of: "Show me stuff about trading"
# Try: "Show me all decisions about risk management"

# Instead of: "What did we do last week?"
# Try: "Generate a team report for Engineering team for last week"
```

### Team Collaboration:
```python
# Set context for team work
eis.authenticate_and_set_context("alice_dev", "auth_token")
eis.set_channel_context("#project-main-development")

# Now all conversations are properly attributed and organized
```

## 🎉 Success Metrics

### Individual Success:
- ✅ Conversations being captured automatically
- ✅ Ability to search and find previous work
- ✅ Insights and decisions properly categorized
- ✅ Session state maintained across conversations

### Team Success:
- ✅ Multiple users active in different channels
- ✅ Cross-team knowledge sharing working
- ✅ Decision traceability showing clear paths
- ✅ Analytics revealing useful patterns

### Enterprise Success:
- ✅ Knowledge graph growing with relationships
- ✅ Search finding relevant information quickly
- ✅ Reports showing team productivity insights
- ✅ Decision audit trail for compliance

---

*💡 Remember: The system gets smarter the more you use it. Start simple with basic capture, then gradually explore the enterprise features as your needs grow!*
# 🧠 Claude Capture System - Enterprise AI Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-windows-lightgrey.svg)](https://www.microsoft.com/windows/)
[![Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)

## 📖 Overview

Transform your Claude conversations into a powerful, searchable enterprise knowledge base! The Claude Capture System automatically captures, analyzes, and organizes all your AI interactions into an intelligent system that gets smarter over time.

## ✨ Key Features

### 🧠 **Smart Conversation Capture**
- **Auto-detection**: Automatically captures all Claude conversations
- **File monitoring**: Tracks modifications and code generation
- **Session management**: Maintains conversation context
- **Windows/Linux compatible**: Works everywhere Claude does

### 🏢 **Enterprise Intelligence** 
- **Knowledge Graph**: Neo4j-powered relationship mapping
- **Team Collaboration**: Multi-user workspace with channels
- **Decision Traceability**: "Show me all insights that led to X"
- **Analytics Dashboard**: Real-time metrics and insights

### 🔍 **Advanced Search & Analytics**
- **Search Everything**: Full-text search across all conversations
- **Insight Extraction**: Automatically identifies key learnings
- **Decision Tracking**: Tracks all decisions and their rationale
- **Team Analytics**: Activity metrics and collaboration insights

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/claude-capture-system.git
cd claude-capture-system

# Install dependencies
pip install -r setup/requirements.txt

# Test the system
.\claude test
```

### Basic Usage
```bash
# Start conversation capture
.\claude start

# Talk to Claude normally - everything is captured automatically!

# Check system status
.\claude status

# Get help
.\claude help
```

### Enterprise Features
```bash
# Launch enterprise intelligence system
.\enterprise_launch.bat

# Or use Python directly
python integrations/enterprise_intelligence_system.py
```

## 🎯 What Makes This Special

### 🧠 **Intelligence Layer**
Unlike simple logging, this system builds an actual **knowledge graph** that:
- Connects related insights and decisions
- Traces the path of every choice made
- Identifies patterns across conversations
- Learns and improves from interactions

### 👥 **Team Collaboration**
Built for teams with:
- User authentication and role-based access
- Channel-based organization (#project-, #research-, #infrastructure-)
- Shared intelligence streams
- Cross-team analytics and reporting

### 🔍 **Enterprise Search**
Find anything instantly with queries like:
- "What decisions did we make about optimization?"
- "Show me all insights from last week"
- "What files were modified when we solved the bug?"
- "Trace the reasoning behind the architecture choice"

## 📁 Project Structure

```
claude-capture-system/
├── claude.bat                     # Main launcher (Windows)
├── claude.ps1                     # Main launcher (PowerShell)
├── README.md                      # This file
├── integrations/                  # Core Python modules
│   ├── seamless_claude_integration_windows.py  # Auto-capture engine
│   ├── enterprise_intelligence_system.py       # Enterprise features
│   ├── knowledge_graph_engine.py              # Intelligence graph
│   ├── multi_agent_collaboration.py           # Team framework
│   └── ...
├── scripts/                       # Management scripts
├── tests/                         # Comprehensive test suite
├── setup/                         # Installation and configuration
├── docs/                          # Complete documentation
└── data/                          # Database storage (created automatically)
```

## 📚 Documentation

### 🎮 **For Beginners**
- **[SUPER_SIMPLE_GUIDE.md](SUPER_SIMPLE_GUIDE.md)** - Explains everything like you're 10!

### 👨‍💻 **For Regular Users**
- **[docs/COMPREHENSIVE_USAGE_GUIDE.md](docs/COMPREHENSIVE_USAGE_GUIDE.md)** - Complete user manual

### 🏢 **For Teams & Enterprises**
- **[ENTERPRISE_DEPLOYMENT_GUIDE.md](ENTERPRISE_DEPLOYMENT_GUIDE.md)** - Team collaboration setup

### 🔧 **For Developers**
- **[docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md)** - Technical architecture
- **[docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)** - All documentation index

## 🎮 Usage Examples

### Basic Conversation Capture
```bash
# Start the system
.\claude start

# System will show: "CLAUDE ACTIVITY DETECTED!" when it captures conversations
# All conversations are automatically stored and analyzed
```

### Enterprise Intelligence Queries
```python
# Search across all conversations and knowledge
from integrations.enterprise_intelligence_system import EnterpriseIntelligenceSystem
eis = EnterpriseIntelligenceSystem()

# Find everything about a topic
results = eis.search_across_systems("optimization strategy")

# Trace decision paths
trace = eis.execute_decision_trace_query("performance improvement")

# Generate team analytics
report = eis.generate_team_intelligence_report("Engineering", "week")
```

### Team Collaboration
```python
# Set up multi-user environment
from integrations.multi_agent_collaboration import MultiAgentCollaborationFramework, UserRole

mcf = MultiAgentCollaborationFramework()

# Create users and channels
admin_id = mcf.create_user("admin", "Admin User", "admin@company.com", UserRole.ADMIN)
mcf.create_default_channels(admin_id)
```

## 🛠️ Technical Requirements

### System Requirements
- **Python 3.8+** with packages: `sqlite3`, `watchdog`, `psutil`
- **Optional**: Neo4j for advanced knowledge graph features
- **Platforms**: Windows 10+, Linux, macOS

### Dependencies
```
sqlite3          # Database storage
watchdog         # File system monitoring
psutil           # Process management
pathlib          # Path handling
json             # Data serialization
neo4j (optional) # Advanced graph database
```

## 🎯 Use Cases

### 👨‍💼 **For Individuals**
- Track all your Claude conversations and learnings
- Search through months of AI interactions instantly
- Never lose important insights or decisions
- Build a personal AI knowledge base

### 👥 **For Teams**
- Share AI discoveries across team members
- Track team decision-making processes
- Collaborate on complex projects with AI assistance
- Generate team productivity analytics

### 🏢 **For Enterprises**
- Enterprise-grade conversation intelligence
- Audit trail for AI-assisted decisions
- Knowledge management across departments
- Compliance and governance for AI usage

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and install
git clone https://github.com/yourusername/claude-capture-system.git
cd claude-capture-system
pip install -r setup/requirements.txt

# Run tests
python tests/test_enterprise_system.py

# Test the system
.\claude test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` folder for comprehensive guides
- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions

## 🎉 Getting Started

1. **Clone this repository**
2. **Install dependencies**: `pip install -r setup/requirements.txt`
3. **Test the system**: `.\claude test`
4. **Start capturing**: `.\claude start`
5. **Explore features**: Read [SUPER_SIMPLE_GUIDE.md](SUPER_SIMPLE_GUIDE.md)

## 🌟 Why Claude Capture System?

Transform scattered AI conversations into organized intelligence. Whether you're an individual user, a team, or an enterprise, this system helps you:

- **Never lose insights** - Every conversation captured and searchable
- **Track decisions** - See the full reasoning behind every choice
- **Collaborate effectively** - Share AI discoveries across your team
- **Scale intelligently** - Enterprise features that grow with your needs

---

**🧠 Transform your Claude conversations into enterprise intelligence • 👥 Built for teams • 🚀 Ready for production**

*Made with ❤️ for the Claude community*
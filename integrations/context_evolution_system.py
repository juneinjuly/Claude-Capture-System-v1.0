#!/usr/bin/env python3
"""
Context Evolution System - Building on Top of Comprehensive Context
Automatically captures and integrates new conversations, discoveries, and insights
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from collections import defaultdict

class ContextEvolutionSystem:
    """
    Manages the evolution of project context by capturing new conversations,
    insights, and discoveries, then integrating them into the comprehensive context.
    """
    
    def __init__(self, project_root: str = None):
        """Initialize the context evolution system"""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        
        # Core files
        self.comprehensive_context = self.project_root / "COMPREHENSIVE_CONTEXT.md"
        self.evolution_log = self.project_root / "CONTEXT_EVOLUTION_LOG.md"
        self.session_tracker = self.project_root / "session_tracker.json"
        self.insights_db = self.project_root / "insights_database.json"
        
        # Evolution directories
        self.sessions_dir = self.project_root / "context_sessions"
        self.insights_dir = self.project_root / "context_insights"
        self.discoveries_dir = self.project_root / "context_discoveries"
        
        # Create directories
        for dir_path in [self.sessions_dir, self.insights_dir, self.discoveries_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize tracking
        self.session_data = self.load_session_tracker()
        self.insights_data = self.load_insights_database()
        
        self.current_session_id = self.generate_session_id()
        self.current_session_insights = []
        
        print(f"🧠 Context Evolution System initialized")
        print(f"📊 Session ID: {self.current_session_id}")
        print(f"🎯 Ready to capture new insights and conversations")
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}"
    
    def load_session_tracker(self) -> Dict[str, Any]:
        """Load session tracking data"""
        if self.session_tracker.exists():
            with open(self.session_tracker, 'r') as f:
                return json.load(f)
        return {
            "sessions": [],
            "last_context_update": None,
            "total_insights": 0,
            "evolution_version": "1.0"
        }
    
    def load_insights_database(self) -> Dict[str, Any]:
        """Load insights database"""
        if self.insights_db.exists():
            with open(self.insights_db, 'r') as f:
                return json.load(f)
        return {
            "insights": [],
            "categories": defaultdict(list),
            "tags": defaultdict(list),
            "cross_references": defaultdict(list)
        }
    
    def save_session_tracker(self):
        """Save session tracking data"""
        with open(self.session_tracker, 'w') as f:
            json.dump(self.session_data, f, indent=2, default=str)
    
    def save_insights_database(self):
        """Save insights database"""
        with open(self.insights_db, 'w') as f:
            json.dump(self.insights_data, f, indent=2, default=str)
    
    def start_session(self, session_purpose: str = "General development"):
        """Start a new context evolution session"""
        session_info = {
            "session_id": self.current_session_id,
            "start_time": datetime.now().isoformat(),
            "purpose": session_purpose,
            "insights_captured": 0,
            "files_modified": [],
            "tests_completed": [],
            "key_discoveries": []
        }
        
        self.session_data["sessions"].append(session_info)
        self.current_session_info = session_info
        
        # Create session file
        session_file = self.sessions_dir / f"{self.current_session_id}.md"
        session_content = f"""# Context Evolution Session: {self.current_session_id}

## Session Info
- **Start Time:** {session_info['start_time']}
- **Purpose:** {session_purpose}
- **Status:** In Progress

## Conversation Log
"""
        
        with open(session_file, 'w') as f:
            f.write(session_content)
        
        print(f"📝 Started session: {self.current_session_id}")
        print(f"🎯 Purpose: {session_purpose}")
        return self.current_session_id
    
    def capture_conversation(self, 
                           user_query: str, 
                           ai_response: str, 
                           insights: List[str] = None,
                           files_discussed: List[str] = None,
                           decisions_made: List[str] = None):
        """Capture a conversation exchange with insights"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract insights if not provided
        if insights is None:
            insights = self.extract_insights_from_conversation(user_query, ai_response)
        
        # Create conversation entry
        conversation_entry = {
            "timestamp": timestamp,
            "user_query": user_query,
            "ai_response": ai_response,
            "insights": insights,
            "files_discussed": files_discussed or [],
            "decisions_made": decisions_made or [],
            "session_id": self.current_session_id
        }
        
        # Add to session file
        session_file = self.sessions_dir / f"{self.current_session_id}.md"
        
        conversation_md = f"""
### Conversation at {timestamp}

**User Query:**
{user_query}

**AI Response:**
{ai_response}

**Key Insights:**
{chr(10).join(f"- {insight}" for insight in insights)}

**Files Discussed:**
{chr(10).join(f"- {file}" for file in files_discussed or [])}

**Decisions Made:**
{chr(10).join(f"- {decision}" for decision in decisions_made or [])}

---
"""
        
        with open(session_file, 'a') as f:
            f.write(conversation_md)
        
        # Store insights for context integration
        for insight in insights:
            self.add_insight(insight, "conversation", files_discussed)
        
        print(f"💬 Captured conversation with {len(insights)} insights")
        return conversation_entry
    
    def extract_insights_from_conversation(self, user_query: str, ai_response: str) -> List[str]:
        """Extract insights from conversation using pattern matching"""
        insights = []
        
        # Patterns to identify insights
        insight_patterns = [
            r"Key finding[s]?:?\s*(.+)",
            r"Strategic implication[s]?:?\s*(.+)",
            r"Important[ly]?:?\s*(.+)",
            r"Critical[ly]?:?\s*(.+)",
            r"Note[d]?:?\s*(.+)",
            r"Insight:?\s*(.+)",
            r"Discovery:?\s*(.+)",
            r"Learning:?\s*(.+)",
            r"Recommendation:?\s*(.+)",
            r"Next step[s]?:?\s*(.+)",
            r"Action item[s]?:?\s*(.+)"
        ]
        
        combined_text = f"{user_query}\n{ai_response}"
        
        for pattern in insight_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE | re.MULTILINE)
            insights.extend(matches)
        
        # Clean and deduplicate
        cleaned_insights = []
        for insight in insights:
            cleaned = insight.strip().rstrip('.')
            if len(cleaned) > 10 and cleaned not in cleaned_insights:
                cleaned_insights.append(cleaned)
        
        return cleaned_insights[:5]  # Limit to top 5 insights
    
    def add_insight(self, 
                   insight: str, 
                   category: str = "general",
                   related_files: List[str] = None,
                   tags: List[str] = None):
        """Add a new insight to the database"""
        
        insight_id = hashlib.md5(insight.encode()).hexdigest()[:8]
        
        insight_record = {
            "id": insight_id,
            "content": insight,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.current_session_id,
            "related_files": related_files or [],
            "tags": tags or [],
            "importance_score": self.calculate_importance_score(insight)
        }
        
        # Add to database
        self.insights_data["insights"].append(insight_record)
        self.insights_data["categories"][category].append(insight_id)
        
        # Add tags
        for tag in tags or []:
            self.insights_data["tags"][tag].append(insight_id)
        
        # Update session counter
        self.session_data["total_insights"] += 1
        
        print(f"💡 Added insight: {insight[:50]}...")
        return insight_id
    
    def calculate_importance_score(self, insight: str) -> float:
        """Calculate importance score for an insight"""
        score = 0.5  # Base score
        
        # High importance keywords
        high_importance = ["critical", "key", "strategic", "important", "breakthrough", "discovery"]
        medium_importance = ["finding", "insight", "recommendation", "note", "learning"]
        
        insight_lower = insight.lower()
        
        for keyword in high_importance:
            if keyword in insight_lower:
                score += 0.3
        
        for keyword in medium_importance:
            if keyword in insight_lower:
                score += 0.1
        
        # Length bonus (longer insights often more valuable)
        if len(insight) > 100:
            score += 0.1
        
        return min(score, 1.0)
    
    def mark_test_completion(self, test_name: str, key_findings: List[str], files_created: List[str]):
        """Mark completion of a test with key findings"""
        
        completion_record = {
            "test_name": test_name,
            "completion_time": datetime.now().isoformat(),
            "session_id": self.current_session_id,
            "key_findings": key_findings,
            "files_created": files_created,
            "status": "completed"
        }
        
        # Add to session
        if hasattr(self, 'current_session_info'):
            self.current_session_info["tests_completed"].append(completion_record)
        
        # Create insights from findings
        for finding in key_findings:
            self.add_insight(finding, "test_completion", files_created, [test_name.lower()])
        
        print(f"✅ Marked test completion: {test_name}")
        print(f"📊 Captured {len(key_findings)} findings")
        
        return completion_record
    
    def create_context_evolution_entry(self, 
                                     change_type: str,
                                     description: str,
                                     impact_level: str = "medium",
                                     related_files: List[str] = None):
        """Create an entry for context evolution"""
        
        entry = {
            "id": hashlib.md5(f"{change_type}_{description}_{datetime.now()}".encode()).hexdigest()[:8],
            "change_type": change_type,  # "new_test", "insight", "discovery", "decision", "file_change"
            "description": description,
            "impact_level": impact_level,  # "low", "medium", "high", "critical"
            "timestamp": datetime.now().isoformat(),
            "session_id": self.current_session_id,
            "related_files": related_files or [],
            "integration_status": "pending"
        }
        
        # Log evolution entry
        evolution_file = self.project_root / "CONTEXT_EVOLUTION_LOG.md"
        
        if not evolution_file.exists():
            with open(evolution_file, 'w') as f:
                f.write("# Context Evolution Log\n\n")
        
        entry_md = f"""## {change_type.upper()}: {description}
- **Timestamp:** {entry['timestamp']}
- **Impact Level:** {impact_level}
- **Session:** {self.current_session_id}
- **Related Files:** {', '.join(related_files or [])}
- **Status:** {entry['integration_status']}

---
"""
        
        with open(evolution_file, 'a') as f:
            f.write(entry_md)
        
        return entry
    
    def integrate_session_insights(self, session_id: str = None):
        """Integrate insights from a session into the comprehensive context"""
        
        if session_id is None:
            session_id = self.current_session_id
        
        # Get session insights
        session_insights = [
            insight for insight in self.insights_data["insights"] 
            if insight["session_id"] == session_id
        ]
        
        if not session_insights:
            print(f"No insights found for session {session_id}")
            return
        
        # Group insights by category
        categorized_insights = defaultdict(list)
        for insight in session_insights:
            categorized_insights[insight["category"]].append(insight)
        
        # Create integration content
        integration_content = f"""
## SESSION INSIGHTS INTEGRATION - {session_id}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### New Insights Added:
"""
        
        for category, insights in categorized_insights.items():
            integration_content += f"\n#### {category.upper()}\n"
            for insight in insights:
                integration_content += f"- {insight['content']}\n"
        
        # Add to comprehensive context
        self.append_to_comprehensive_context(integration_content)
        
        # Mark insights as integrated
        for insight in session_insights:
            insight["integration_status"] = "integrated"
        
        # Update session data
        self.session_data["last_context_update"] = datetime.now().isoformat()
        self.save_session_tracker()
        self.save_insights_database()
        
        print(f"🔄 Integrated {len(session_insights)} insights into comprehensive context")
        return integration_content
    
    def append_to_comprehensive_context(self, content: str):
        """Append new content to the comprehensive context file"""
        
        # Read current context
        with open(self.comprehensive_context, 'r') as f:
            current_content = f.read()
        
        # Find insertion point (before the final "Begin user prompt below")
        insertion_point = "# [END OF COMPREHENSIVE CONTEXT] - Begin user prompt below:"
        
        if insertion_point in current_content:
            # Insert before the end marker
            new_content = current_content.replace(
                insertion_point,
                f"{content}\n\n{insertion_point}"
            )
        else:
            # Append at the end
            new_content = current_content + "\n\n" + content
        
        # Write updated content
        with open(self.comprehensive_context, 'w') as f:
            f.write(new_content)
        
        print(f"📝 Updated comprehensive context with new content")
    
    def end_session(self, session_summary: str = None):
        """End the current session and integrate insights"""
        
        if hasattr(self, 'current_session_info'):
            self.current_session_info["end_time"] = datetime.now().isoformat()
            self.current_session_info["status"] = "completed"
            self.current_session_info["summary"] = session_summary or "Session completed"
            
            # Integrate session insights
            self.integrate_session_insights()
            
            # Update session file
            session_file = self.sessions_dir / f"{self.current_session_id}.md"
            
            summary_content = f"""
## Session Summary
- **End Time:** {self.current_session_info['end_time']}
- **Total Insights:** {self.current_session_info['insights_captured']}
- **Tests Completed:** {len(self.current_session_info.get('tests_completed', []))}
- **Files Modified:** {len(self.current_session_info.get('files_modified', []))}

**Summary:** {session_summary or 'Session completed successfully'}

## Session Complete ✅
"""
            
            with open(session_file, 'a') as f:
                f.write(summary_content)
        
        self.save_session_tracker()
        self.save_insights_database()
        
        print(f"🏁 Session ended: {self.current_session_id}")
        print(f"📊 Total insights captured: {self.session_data['total_insights']}")
        
        return self.current_session_id
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get summary of context evolution"""
        
        recent_sessions = [
            s for s in self.session_data["sessions"] 
            if datetime.fromisoformat(s["start_time"]) > datetime.now() - timedelta(days=7)
        ]
        
        high_importance_insights = [
            i for i in self.insights_data["insights"] 
            if i["importance_score"] > 0.8
        ]
        
        return {
            "total_sessions": len(self.session_data["sessions"]),
            "recent_sessions": len(recent_sessions),
            "total_insights": len(self.insights_data["insights"]),
            "high_importance_insights": len(high_importance_insights),
            "categories": list(self.insights_data["categories"].keys()),
            "last_update": self.session_data.get("last_context_update"),
            "evolution_version": self.session_data.get("evolution_version")
        }
    
    def search_insights(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search insights database"""
        
        results = []
        query_lower = query.lower()
        
        for insight in self.insights_data["insights"]:
            if category and insight["category"] != category:
                continue
            
            if query_lower in insight["content"].lower():
                results.append(insight)
        
        # Sort by importance score
        results.sort(key=lambda x: x["importance_score"], reverse=True)
        
        return results


def main():
    """CLI interface for context evolution system"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Context Evolution System")
    parser.add_argument("--start", type=str, help="Start new session with purpose")
    parser.add_argument("--end", type=str, help="End current session with summary")
    parser.add_argument("--capture", action="store_true", help="Capture conversation")
    parser.add_argument("--integrate", action="store_true", help="Integrate current session")
    parser.add_argument("--summary", action="store_true", help="Show evolution summary")
    parser.add_argument("--search", type=str, help="Search insights")
    
    args = parser.parse_args()
    
    ces = ContextEvolutionSystem()
    
    if args.start:
        ces.start_session(args.start)
    elif args.end:
        ces.end_session(args.end)
    elif args.integrate:
        ces.integrate_session_insights()
    elif args.summary:
        summary = ces.get_evolution_summary()
        print(json.dumps(summary, indent=2))
    elif args.search:
        results = ces.search_insights(args.search)
        print(f"Found {len(results)} insights:")
        for result in results[:5]:
            print(f"- {result['content']}")
    else:
        summary = ces.get_evolution_summary()
        print("Context Evolution System Status:")
        for key, value in summary.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
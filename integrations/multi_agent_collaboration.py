#!/usr/bin/env python3
"""
Multi-Agent Collaboration Framework - The People Layer
Enables team-wide intelligence sharing with user authentication, channels, and analytics
"""

import json
import sqlite3
import time
import hashlib
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import re

class UserRole(Enum):
    """User roles in the system"""
    ADMIN = "admin"
    SENIOR_PM = "senior_pm"
    RESEARCHER = "researcher"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"

class ChannelType(Enum):
    """Types of intelligence channels"""
    PROJECT = "project"
    RESEARCH = "research"
    INFRASTRUCTURE = "infrastructure"
    STRATEGY = "strategy"
    GENERAL = "general"

class MultiAgentCollaborationFramework:
    """
    Multi-user collaboration framework for enterprise-wide intelligence sharing
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.collaboration_db = self.project_root / "claude_capture" / "data" / "claude_collaboration.db"
        
        # Initialize collaboration database
        self.init_collaboration_database()
        
        # Cache for active sessions
        self.active_sessions = {}
        
        # Channel prefixes
        self.channel_prefixes = {
            ChannelType.PROJECT: "#project-",
            ChannelType.RESEARCH: "#research-",
            ChannelType.INFRASTRUCTURE: "#infrastructure-",
            ChannelType.STRATEGY: "#strategy-",
            ChannelType.GENERAL: "#general-"
        }
    
    def init_collaboration_database(self):
        """Initialize the collaboration database with user, channel, and permission tables"""
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                email TEXT UNIQUE,
                role TEXT NOT NULL,
                team TEXT,
                auth_token_hash TEXT,
                created_at TEXT,
                last_active TEXT,
                is_active INTEGER DEFAULT 1,
                metadata TEXT
            )
        ''')
        
        # Agents table (for AI agents)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                agent_name TEXT UNIQUE NOT NULL,
                agent_type TEXT,
                owner_user_id TEXT,
                capabilities TEXT,
                created_at TEXT,
                last_active TEXT,
                is_active INTEGER DEFAULT 1,
                metadata TEXT,
                FOREIGN KEY (owner_user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Channels table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                channel_id TEXT PRIMARY KEY,
                channel_name TEXT UNIQUE NOT NULL,
                channel_type TEXT,
                description TEXT,
                created_by TEXT,
                created_at TEXT,
                is_public INTEGER DEFAULT 1,
                is_active INTEGER DEFAULT 1,
                metadata TEXT,
                FOREIGN KEY (created_by) REFERENCES users (user_id)
            )
        ''')
        
        # Channel memberships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channel_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT,
                user_id TEXT,
                joined_at TEXT,
                role TEXT DEFAULT 'member',
                FOREIGN KEY (channel_id) REFERENCES channels (channel_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(channel_id, user_id)
            )
        ''')
        
        # Intelligence entries (conversations with attribution)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intelligence_entries (
                entry_id TEXT PRIMARY KEY,
                channel_id TEXT,
                user_id TEXT,
                agent_id TEXT,
                entry_type TEXT,
                content TEXT,
                file_path TEXT,
                insights_extracted TEXT,
                decisions_made TEXT,
                timestamp TEXT,
                conversation_id TEXT,
                importance_score REAL DEFAULT 0.0,
                metadata TEXT,
                FOREIGN KEY (channel_id) REFERENCES channels (channel_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (agent_id) REFERENCES agents (agent_id)
            )
        ''')
        
        # Team analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT,
                team TEXT,
                user_id TEXT,
                channel_id TEXT,
                metric_value REAL,
                time_period TEXT,
                calculated_at TEXT,
                metadata TEXT
            )
        ''')
        
        # Access control table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_control (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_type TEXT,
                resource_id TEXT,
                user_id TEXT,
                permission TEXT,
                granted_by TEXT,
                granted_at TEXT,
                expires_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (granted_by) REFERENCES users (user_id)
            )
        ''')
        
        # Intelligence search index
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id TEXT,
                searchable_text TEXT,
                tags TEXT,
                indexed_at TEXT,
                FOREIGN KEY (entry_id) REFERENCES intelligence_entries (entry_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("SUCCESS: Multi-agent collaboration database initialized")
    
    def create_user(self, username: str, full_name: str, email: str, 
                   role: UserRole, team: str = None) -> str:
        """Create a new user in the system"""
        user_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        auth_token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (user_id, username, full_name, email, role, team, 
                                 auth_token_hash, created_at, last_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, username, full_name, email, role.value, team,
                auth_token_hash, timestamp, timestamp
            ))
            
            conn.commit()
            print(f"SUCCESS: Created user {username} with role {role.value}")
            
        except sqlite3.IntegrityError as e:
            print(f"ERROR: User creation failed - {e}")
            return None
        finally:
            conn.close()
        
        return user_id
    
    def create_agent(self, agent_name: str, agent_type: str, 
                    owner_user_id: str, capabilities: List[str]) -> str:
        """Create a new AI agent in the system"""
        agent_id = f"agent_{uuid.uuid4()}"
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO agents (agent_id, agent_name, agent_type, owner_user_id, 
                                  capabilities, created_at, last_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent_id, agent_name, agent_type, owner_user_id,
                json.dumps(capabilities), timestamp, timestamp
            ))
            
            conn.commit()
            print(f"SUCCESS: Created agent {agent_name} of type {agent_type}")
            
        except sqlite3.IntegrityError as e:
            print(f"ERROR: Agent creation failed - {e}")
            return None
        finally:
            conn.close()
        
        return agent_id
    
    def create_channel(self, channel_name: str, channel_type: ChannelType, 
                      description: str, created_by: str, is_public: bool = True) -> str:
        """Create a new intelligence channel"""
        channel_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Ensure channel name follows convention
        prefix = self.channel_prefixes.get(channel_type, "#")
        if not channel_name.startswith(prefix):
            channel_name = prefix + channel_name
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO channels (channel_id, channel_name, channel_type, description, 
                                    created_by, created_at, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                channel_id, channel_name, channel_type.value, description,
                created_by, timestamp, int(is_public)
            ))
            
            # Add creator as channel admin
            cursor.execute('''
                INSERT INTO channel_members (channel_id, user_id, joined_at, role)
                VALUES (?, ?, ?, ?)
            ''', (channel_id, created_by, timestamp, 'admin'))
            
            conn.commit()
            print(f"SUCCESS: Created channel {channel_name}")
            
        except sqlite3.IntegrityError as e:
            print(f"ERROR: Channel creation failed - {e}")
            return None
        finally:
            conn.close()
        
        return channel_id
    
    def join_channel(self, user_id: str, channel_id: str, role: str = 'member') -> bool:
        """Add a user to a channel"""
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO channel_members (channel_id, user_id, joined_at, role)
                VALUES (?, ?, ?, ?)
            ''', (channel_id, user_id, timestamp, role))
            
            conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            print(f"ERROR: User {user_id} already in channel {channel_id}")
            return False
        finally:
            conn.close()
    
    def record_intelligence_entry(self, channel_id: str, user_id: str = None, 
                                agent_id: str = None, entry_type: str = 'conversation',
                                content: str = '', file_path: str = None,
                                conversation_id: str = None, 
                                importance_score: float = 0.0) -> str:
        """Record an intelligence entry in a channel"""
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Extract insights and decisions from content
        insights = self.extract_insights(content)
        decisions = self.extract_decisions(content)
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO intelligence_entries (entry_id, channel_id, user_id, agent_id, 
                                            entry_type, content, file_path, insights_extracted,
                                            decisions_made, timestamp, conversation_id, 
                                            importance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry_id, channel_id, user_id, agent_id, entry_type, content, file_path,
            json.dumps(insights), json.dumps(decisions), timestamp, 
            conversation_id, importance_score
        ))
        
        # Update search index
        self.update_search_index(entry_id, content, insights + decisions)
        
        # Update user/agent last active
        if user_id:
            cursor.execute("UPDATE users SET last_active = ? WHERE user_id = ?", 
                         (timestamp, user_id))
        if agent_id:
            cursor.execute("UPDATE agents SET last_active = ? WHERE agent_id = ?", 
                         (timestamp, agent_id))
        
        conn.commit()
        conn.close()
        
        print(f"INTELLIGENCE: Recorded entry in channel {channel_id}")
        return entry_id
    
    def extract_insights(self, content: str) -> List[str]:
        """Extract insights from content"""
        insight_patterns = [
            r"insight:?\s*(.+?)(?:\n|$)",
            r"learned:?\s*(.+?)(?:\n|$)",
            r"discovered:?\s*(.+?)(?:\n|$)",
            r"found that\s*(.+?)(?:\n|$)"
        ]
        
        insights = []
        for pattern in insight_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            insights.extend([match.strip() for match in matches])
        
        return insights
    
    def extract_decisions(self, content: str) -> List[str]:
        """Extract decisions from content"""
        decision_patterns = [
            r"decided:?\s*(.+?)(?:\n|$)",
            r"decision:?\s*(.+?)(?:\n|$)",
            r"will implement\s*(.+?)(?:\n|$)",
            r"agreed to\s*(.+?)(?:\n|$)"
        ]
        
        decisions = []
        for pattern in decision_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            decisions.extend([match.strip() for match in matches])
        
        return decisions
    
    def update_search_index(self, entry_id: str, content: str, tags: List[str]):
        """Update the search index for an entry"""
        timestamp = datetime.now().isoformat()
        searchable_text = content.lower()
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_index (entry_id, searchable_text, tags, indexed_at)
            VALUES (?, ?, ?, ?)
        ''', (entry_id, searchable_text, json.dumps(tags), timestamp))
        
        conn.commit()
        conn.close()
    
    def search_intelligence(self, query: str, user_id: str, 
                          channel_ids: List[str] = None, 
                          time_range: Tuple[datetime, datetime] = None) -> List[Dict]:
        """Search across intelligence entries with user permissions"""
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        # Build search query
        search_query = '''
            SELECT DISTINCT ie.* FROM intelligence_entries ie
            JOIN search_index si ON ie.entry_id = si.entry_id
            JOIN channel_members cm ON ie.channel_id = cm.channel_id
            WHERE cm.user_id = ? AND si.searchable_text LIKE ?
        '''
        
        params = [user_id, f'%{query.lower()}%']
        
        if channel_ids:
            placeholders = ','.join(['?' for _ in channel_ids])
            search_query += f' AND ie.channel_id IN ({placeholders})'
            params.extend(channel_ids)
        
        if time_range:
            search_query += ' AND ie.timestamp BETWEEN ? AND ?'
            params.extend([time_range[0].isoformat(), time_range[1].isoformat()])
        
        search_query += ' ORDER BY ie.timestamp DESC LIMIT 100'
        
        cursor.execute(search_query, params)
        results = []
        
        for row in cursor.fetchall():
            results.append({
                'entry_id': row[0],
                'channel_id': row[1],
                'user_id': row[2],
                'agent_id': row[3],
                'entry_type': row[4],
                'content': row[5],
                'file_path': row[6],
                'insights': json.loads(row[7]) if row[7] else [],
                'decisions': json.loads(row[8]) if row[8] else [],
                'timestamp': row[9],
                'importance_score': row[11]
            })
        
        conn.close()
        return results
    
    def generate_team_analytics(self, team: str = None, time_period: str = 'week') -> Dict:
        """Generate analytics for a team or the entire organization"""
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        # Calculate time range
        end_date = datetime.now()
        if time_period == 'day':
            start_date = end_date - timedelta(days=1)
        elif time_period == 'week':
            start_date = end_date - timedelta(weeks=1)
        elif time_period == 'month':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=7)
        
        analytics = {}
        
        # Most active users
        query = '''
            SELECT u.username, u.team, COUNT(ie.entry_id) as entry_count
            FROM users u
            JOIN intelligence_entries ie ON u.user_id = ie.user_id
            WHERE ie.timestamp BETWEEN ? AND ?
        '''
        params = [start_date.isoformat(), end_date.isoformat()]
        
        if team:
            query += ' AND u.team = ?'
            params.append(team)
        
        query += ' GROUP BY u.user_id ORDER BY entry_count DESC LIMIT 10'
        
        cursor.execute(query, params)
        analytics['most_active_users'] = cursor.fetchall()
        
        # Most active channels
        cursor.execute('''
            SELECT c.channel_name, COUNT(ie.entry_id) as entry_count
            FROM channels c
            JOIN intelligence_entries ie ON c.channel_id = ie.channel_id
            WHERE ie.timestamp BETWEEN ? AND ?
            GROUP BY c.channel_id
            ORDER BY entry_count DESC
            LIMIT 10
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        analytics['most_active_channels'] = cursor.fetchall()
        
        # Decision velocity (decisions per day)
        cursor.execute('''
            SELECT DATE(timestamp) as date, 
                   SUM(CASE WHEN json_array_length(decisions_made) > 0 THEN json_array_length(decisions_made) ELSE 0 END) as decision_count
            FROM intelligence_entries
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY DATE(timestamp)
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        analytics['decision_velocity'] = cursor.fetchall()
        
        # Insight generation rate
        cursor.execute('''
            SELECT DATE(timestamp) as date, 
                   SUM(CASE WHEN json_array_length(insights_extracted) > 0 THEN json_array_length(insights_extracted) ELSE 0 END) as insight_count
            FROM intelligence_entries
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY DATE(timestamp)
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        analytics['insight_generation'] = cursor.fetchall()
        
        # Store analytics
        timestamp = datetime.now().isoformat()
        for metric_type, data in analytics.items():
            cursor.execute('''
                INSERT INTO team_analytics (metric_type, team, metric_value, time_period, calculated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (metric_type, team, len(data), time_period, timestamp, json.dumps(data)))
        
        conn.commit()
        conn.close()
        
        return analytics
    
    def get_user_permissions(self, user_id: str) -> Dict:
        """Get all permissions for a user"""
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        # Get user role
        cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
        user_role = cursor.fetchone()
        
        if not user_role:
            return {}
        
        # Get channel memberships
        cursor.execute('''
            SELECT c.channel_name, cm.role
            FROM channel_members cm
            JOIN channels c ON cm.channel_id = c.channel_id
            WHERE cm.user_id = ?
        ''', (user_id,))
        
        channels = cursor.fetchall()
        
        # Get explicit permissions
        cursor.execute('''
            SELECT resource_type, resource_id, permission
            FROM access_control
            WHERE user_id = ? AND (expires_at IS NULL OR expires_at > ?)
        ''', (user_id, datetime.now().isoformat()))
        
        permissions = cursor.fetchall()
        
        conn.close()
        
        return {
            'role': user_role[0],
            'channels': channels,
            'permissions': permissions
        }
    
    def create_default_channels(self, admin_user_id: str):
        """Create default channels for the organization"""
        default_channels = [
            ("aie-core", ChannelType.PROJECT, "Core AIE development and discussions"),
            ("research-new-signals", ChannelType.RESEARCH, "Research on new trading signals"),
            ("infrastructure-devops", ChannelType.INFRASTRUCTURE, "Infrastructure and DevOps discussions"),
            ("strategy-planning", ChannelType.STRATEGY, "Strategic planning and roadmap"),
            ("general", ChannelType.GENERAL, "General discussions and announcements")
        ]
        
        for channel_name, channel_type, description in default_channels:
            self.create_channel(channel_name, channel_type, description, admin_user_id)
    
    def authenticate_user(self, username: str, auth_token: str) -> Optional[str]:
        """Authenticate a user with their token"""
        auth_token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
        
        conn = sqlite3.connect(self.collaboration_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id FROM users 
            WHERE username = ? AND auth_token_hash = ? AND is_active = 1
        ''', (username, auth_token_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None

def main():
    """Main function for testing"""
    mcf = MultiAgentCollaborationFramework()
    
    # Create test users
    admin_id = mcf.create_user("admin", "System Admin", "admin@firm.com", UserRole.ADMIN, "Platform")
    pm_id = mcf.create_user("john_pm", "John Smith", "john@firm.com", UserRole.SENIOR_PM, "Strategy")
    dev_id = mcf.create_user("sarah_dev", "Sarah Chen", "sarah@firm.com", UserRole.DEVELOPER, "Engineering")
    
    # Create test agent
    agent_id = mcf.create_agent("Claude-AIE", "research_assistant", admin_id, 
                               ["code_generation", "analysis", "documentation"])
    
    # Create default channels
    mcf.create_default_channels(admin_id)
    
    # Get channel IDs
    conn = sqlite3.connect(mcf.collaboration_db)
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM channels WHERE channel_name = ?", ("#project-aie-core",))
    project_channel_id = cursor.fetchone()[0]
    conn.close()
    
    # Add users to channel
    mcf.join_channel(pm_id, project_channel_id)
    mcf.join_channel(dev_id, project_channel_id)
    
    # Record some intelligence entries
    mcf.record_intelligence_entry(
        project_channel_id, dev_id, None, "code_commit",
        "Implemented new risk calculation with 60-day lookback. Decision: Use pandas rolling window for efficiency.",
        "risk_calculator.py", importance_score=0.8
    )
    
    mcf.record_intelligence_entry(
        project_channel_id, None, agent_id, "analysis",
        "Insight: The 60-day lookback period shows 15% better signal-to-noise ratio than 30-day period.",
        importance_score=0.9
    )
    
    # Search intelligence
    results = mcf.search_intelligence("60-day lookback", dev_id)
    print(f"SEARCH: Found {len(results)} results for '60-day lookback'")
    
    # Generate analytics
    analytics = mcf.generate_team_analytics()
    print("ANALYTICS:", json.dumps(analytics, indent=2))
    
    print("SUCCESS: Multi-agent collaboration framework initialized")

if __name__ == "__main__":
    main()
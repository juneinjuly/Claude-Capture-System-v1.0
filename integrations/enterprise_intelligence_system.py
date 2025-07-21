#!/usr/bin/env python3
"""
Enterprise Intelligence System - Integration Layer
Combines Knowledge Graph and Multi-Agent Collaboration for complete intelligence platform
"""

import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import threading
import queue

from knowledge_graph_engine import KnowledgeGraphEngine
from multi_agent_collaboration import MultiAgentCollaborationFramework, UserRole, ChannelType
from seamless_claude_integration_windows import SeamlessClaudeIntegration

class EnterpriseIntelligenceSystem:
    """
    Complete enterprise intelligence system combining:
    - Knowledge Graph (Intelligence Layer)
    - Multi-Agent Collaboration (People Layer)
    - Seamless Capture (Data Layer)
    """
    
    def __init__(self, project_root: str = None, neo4j_config: Dict = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        
        # Initialize components
        self.knowledge_graph = KnowledgeGraphEngine(
            project_root, 
            neo4j_config.get('uri') if neo4j_config else None,
            neo4j_config.get('user') if neo4j_config else None,
            neo4j_config.get('password') if neo4j_config else None
        )
        
        self.collaboration = MultiAgentCollaborationFramework(project_root)
        self.capture_system = SeamlessClaudeIntegration(project_root)
        
        # Processing queue for async operations
        self.processing_queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.processing_thread.start()
        
        # Current context
        self.current_user_id = None
        self.current_channel_id = None
        self.current_session_id = None
        
        print("SUCCESS: Enterprise Intelligence System initialized")
    
    def authenticate_and_set_context(self, username: str, auth_token: str) -> bool:
        """Authenticate user and set current context"""
        user_id = self.collaboration.authenticate_user(username, auth_token)
        if user_id:
            self.current_user_id = user_id
            print(f"AUTH: User {username} authenticated")
            return True
        return False
    
    def set_channel_context(self, channel_name: str) -> bool:
        """Set the current channel context"""
        conn = sqlite3.connect(self.collaboration.collaboration_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.channel_id 
            FROM channels c
            JOIN channel_members cm ON c.channel_id = cm.channel_id
            WHERE c.channel_name = ? AND cm.user_id = ?
        """, (channel_name, self.current_user_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.current_channel_id = result[0]
            print(f"CONTEXT: Set channel to {channel_name}")
            return True
        return False
    
    def capture_and_process_conversation(self, file_path: str, content: str, 
                                       conversation_id: str = None) -> Dict:
        """
        Capture a conversation and process it through the entire intelligence pipeline
        """
        if not self.current_user_id or not self.current_channel_id:
            print("ERROR: No user or channel context set")
            return {}
        
        # Record in collaboration system
        entry_id = self.collaboration.record_intelligence_entry(
            self.current_channel_id,
            self.current_user_id,
            None,  # agent_id
            'conversation',
            content,
            file_path,
            conversation_id,
            self._calculate_importance_score(content)
        )
        
        # Process through knowledge graph
        graph_result = self.knowledge_graph.process_conversation_for_graph(
            conversation_id or entry_id,
            content,
            file_path,
            self.current_session_id
        )
        
        # Create cross-system relationships
        self._create_cross_system_relationships(entry_id, graph_result)
        
        return {
            'entry_id': entry_id,
            'graph_nodes': graph_result,
            'channel': self.current_channel_id,
            'user': self.current_user_id
        }
    
    def _calculate_importance_score(self, content: str) -> float:
        """Calculate importance score based on content analysis"""
        score = 0.5  # Base score
        
        # Boost for insights
        if any(keyword in content.lower() for keyword in ['insight', 'discovered', 'learned']):
            score += 0.2
        
        # Boost for decisions
        if any(keyword in content.lower() for keyword in ['decision', 'decided', 'will implement']):
            score += 0.3
        
        # Boost for action items
        if any(keyword in content.lower() for keyword in ['todo', 'action item', 'next step']):
            score += 0.1
        
        return min(score, 1.0)
    
    def _create_cross_system_relationships(self, entry_id: str, graph_result: Dict):
        """Create relationships between collaboration entries and knowledge graph nodes"""
        # Queue for async processing
        self.processing_queue.put({
            'type': 'cross_system_relationships',
            'entry_id': entry_id,
            'graph_result': graph_result
        })
    
    def _process_queue(self):
        """Background processor for async operations"""
        while True:
            try:
                task = self.processing_queue.get(timeout=1)
                
                if task['type'] == 'cross_system_relationships':
                    # Create relationships between systems
                    entry_id = task['entry_id']
                    graph_result = task['graph_result']
                    
                    # Link insights to collaboration entry
                    for insight_id in graph_result.get('insights', []):
                        self.knowledge_graph.create_relationship(
                            insight_id, entry_id, 'CAPTURED_IN_ENTRY', 
                            {'system': 'collaboration'}, 0.8
                        )
                    
                    # Link decisions to collaboration entry
                    for decision_id in graph_result.get('decisions', []):
                        self.knowledge_graph.create_relationship(
                            decision_id, entry_id, 'RECORDED_IN_ENTRY',
                            {'system': 'collaboration'}, 0.8
                        )
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"ERROR: Queue processing error: {e}")
    
    def execute_decision_trace_query(self, decision_content: str) -> Dict:
        """
        Execute the powerful decision traceability query
        Example: "Show me all insights that led to using 60-day lookback"
        """
        # Find decision nodes matching content
        conn = sqlite3.connect(self.knowledge_graph.graph_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content, source_file_path 
            FROM nodes 
            WHERE type = 'Decision' AND content LIKE ?
        """, (f'%{decision_content}%',))
        
        decisions = cursor.fetchall()
        
        if not decisions:
            return {'error': 'No matching decisions found'}
        
        results = {}
        for decision in decisions:
            decision_id = decision[0]
            
            # Trace the decision path
            trace = self.knowledge_graph.trace_decision_path(decision_id)
            
            # Get collaboration context
            cursor.execute("""
                SELECT ie.channel_id, ie.user_id, ie.timestamp, c.channel_name, u.username
                FROM intelligence_entries ie
                JOIN channels c ON ie.channel_id = c.channel_id
                JOIN users u ON ie.user_id = u.user_id
                WHERE ie.content LIKE ?
                ORDER BY ie.timestamp DESC
                LIMIT 5
            """, (f'%{decision[2][:50]}%',))
            
            collaboration_context = cursor.fetchall()
            
            results[decision_id] = {
                'decision': {
                    'id': decision[0],
                    'title': decision[1],
                    'content': decision[2],
                    'file': decision[3]
                },
                'insights': trace.get('insights', []),
                'affected_files': trace.get('files', []),
                'collaboration_context': collaboration_context
            }
        
        conn.close()
        return results
    
    def generate_team_intelligence_report(self, team: str = None, 
                                        time_period: str = 'week') -> Dict:
        """Generate comprehensive intelligence report for a team"""
        # Get collaboration analytics
        collab_analytics = self.collaboration.generate_team_analytics(team, time_period)
        
        # Get knowledge graph analytics
        graph_analytics = self.knowledge_graph.generate_graph_analytics()
        
        # Combine and analyze
        report = {
            'team': team or 'All Teams',
            'time_period': time_period,
            'generated_at': datetime.now().isoformat(),
            'collaboration_metrics': collab_analytics,
            'knowledge_graph_metrics': graph_analytics,
            'key_insights': [],
            'critical_decisions': [],
            'action_items_pending': []
        }
        
        # Extract key insights from recent high-importance entries
        conn = sqlite3.connect(self.collaboration.collaboration_db)
        cursor = conn.cursor()
        
        query = """
            SELECT insights_extracted, decisions_made, importance_score
            FROM intelligence_entries
            WHERE importance_score > 0.7
        """
        
        if team:
            query += " AND user_id IN (SELECT user_id FROM users WHERE team = ?)"
            cursor.execute(query + " ORDER BY timestamp DESC LIMIT 20", (team,))
        else:
            cursor.execute(query + " ORDER BY timestamp DESC LIMIT 20")
        
        for row in cursor.fetchall():
            if row[0]:  # insights
                insights = json.loads(row[0])
                report['key_insights'].extend(insights[:2])  # Top 2 insights
            if row[1]:  # decisions
                decisions = json.loads(row[1])
                report['critical_decisions'].extend(decisions[:1])  # Top decision
        
        conn.close()
        
        return report
    
    def search_across_systems(self, query: str, search_type: str = 'all') -> Dict:
        """
        Unified search across both collaboration and knowledge graph
        """
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'collaboration_results': [],
            'knowledge_graph_results': [],
            'combined_insights': []
        }
        
        if search_type in ['all', 'collaboration']:
            # Search collaboration system
            collab_results = self.collaboration.search_intelligence(
                query, self.current_user_id
            )
            results['collaboration_results'] = collab_results
        
        if search_type in ['all', 'graph']:
            # Search knowledge graph
            conn = sqlite3.connect(self.knowledge_graph.graph_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM nodes 
                WHERE content LIKE ? OR title LIKE ?
                ORDER BY confidence DESC
                LIMIT 20
            """, (f'%{query}%', f'%{query}%'))
            
            graph_results = cursor.fetchall()
            results['knowledge_graph_results'] = [
                {
                    'id': row[0],
                    'type': row[1],
                    'title': row[2],
                    'content': row[3],
                    'confidence': row[9]
                }
                for row in graph_results
            ]
            
            conn.close()
        
        # Combine insights
        all_insights = []
        for collab in results['collaboration_results']:
            all_insights.extend(collab.get('insights', []))
        
        for graph in results['knowledge_graph_results']:
            if graph['type'] == 'Insight':
                all_insights.append(graph['content'])
        
        # Deduplicate and rank
        seen = set()
        unique_insights = []
        for insight in all_insights:
            if insight not in seen:
                seen.add(insight)
                unique_insights.append(insight)
        
        results['combined_insights'] = unique_insights[:10]
        
        return results
    
    def create_intelligence_dashboard_data(self) -> Dict:
        """Generate data for an intelligence dashboard"""
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'system_health': self._check_system_health(),
            'real_time_metrics': {},
            'recent_activity': [],
            'trending_topics': [],
            'team_leaderboard': []
        }
        
        # Real-time metrics
        conn_collab = sqlite3.connect(self.collaboration.collaboration_db)
        cursor_collab = conn_collab.cursor()
        
        # Active users in last hour
        cursor_collab.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM intelligence_entries 
            WHERE timestamp > datetime('now', '-1 hour')
        """)
        dashboard_data['real_time_metrics']['active_users_1h'] = cursor_collab.fetchone()[0]
        
        # Entries in last 24 hours
        cursor_collab.execute("""
            SELECT COUNT(*) 
            FROM intelligence_entries 
            WHERE timestamp > datetime('now', '-24 hours')
        """)
        dashboard_data['real_time_metrics']['entries_24h'] = cursor_collab.fetchone()[0]
        
        # Recent activity stream
        cursor_collab.execute("""
            SELECT u.username, c.channel_name, ie.entry_type, ie.timestamp
            FROM intelligence_entries ie
            JOIN users u ON ie.user_id = u.user_id
            JOIN channels c ON ie.channel_id = c.channel_id
            ORDER BY ie.timestamp DESC
            LIMIT 10
        """)
        
        dashboard_data['recent_activity'] = [
            {
                'user': row[0],
                'channel': row[1],
                'type': row[2],
                'timestamp': row[3]
            }
            for row in cursor_collab.fetchall()
        ]
        
        # Team leaderboard
        cursor_collab.execute("""
            SELECT u.team, COUNT(ie.entry_id) as contributions,
                   AVG(ie.importance_score) as avg_importance
            FROM users u
            JOIN intelligence_entries ie ON u.user_id = ie.user_id
            WHERE ie.timestamp > datetime('now', '-7 days')
            GROUP BY u.team
            ORDER BY contributions DESC
            LIMIT 5
        """)
        
        dashboard_data['team_leaderboard'] = [
            {
                'team': row[0],
                'contributions': row[1],
                'avg_importance': round(row[2], 2) if row[2] else 0
            }
            for row in cursor_collab.fetchall()
        ]
        
        conn_collab.close()
        
        # Knowledge graph metrics
        graph_analytics = self.knowledge_graph.generate_graph_analytics()
        dashboard_data['knowledge_graph_stats'] = {
            'total_nodes': graph_analytics['total_nodes'],
            'total_relationships': graph_analytics['total_relationships'],
            'node_distribution': graph_analytics['node_counts']
        }
        
        return dashboard_data
    
    def _check_system_health(self) -> Dict:
        """Check health of all system components"""
        health = {
            'capture_system': 'unknown',
            'knowledge_graph': 'unknown',
            'collaboration': 'unknown',
            'overall': 'unknown'
        }
        
        # Check capture system
        try:
            if hasattr(self.capture_system, 'session_data'):
                health['capture_system'] = 'healthy'
        except:
            health['capture_system'] = 'error'
        
        # Check knowledge graph
        try:
            conn = sqlite3.connect(self.knowledge_graph.graph_db)
            conn.execute("SELECT COUNT(*) FROM nodes")
            conn.close()
            health['knowledge_graph'] = 'healthy'
        except:
            health['knowledge_graph'] = 'error'
        
        # Check collaboration
        try:
            conn = sqlite3.connect(self.collaboration.collaboration_db)
            conn.execute("SELECT COUNT(*) FROM users")
            conn.close()
            health['collaboration'] = 'healthy'
        except:
            health['collaboration'] = 'error'
        
        # Overall health
        if all(v == 'healthy' for v in health.values() if v != 'unknown'):
            health['overall'] = 'healthy'
        elif any(v == 'error' for v in health.values()):
            health['overall'] = 'degraded'
        else:
            health['overall'] = 'unknown'
        
        return health

def main():
    """Demonstration of the Enterprise Intelligence System"""
    
    # Initialize system
    eis = EnterpriseIntelligenceSystem()
    
    # Create test users and setup
    mcf = eis.collaboration
    admin_id = mcf.create_user("admin", "System Admin", "admin@firm.com", UserRole.ADMIN, "Platform")
    dev_id = mcf.create_user("alice_dev", "Alice Johnson", "alice@firm.com", UserRole.DEVELOPER, "Engineering")
    
    # Create channels
    mcf.create_default_channels(admin_id)
    
    # Authenticate as developer
    eis.current_user_id = dev_id
    eis.set_channel_context("#project-aie-core")
    
    # Simulate capturing a conversation
    sample_content = """
    After extensive testing, we discovered that the 60-day lookback period provides 
    optimal signal strength for our momentum indicators.
    
    Decision: Implement 60-day lookback across all momentum-based strategies.
    
    TODO: Update risk_calculator.py with new lookback parameter
    TODO: Run full backtest suite with new parameters
    
    Insight: Longer lookback periods reduce noise but may miss short-term opportunities.
    """
    
    result = eis.capture_and_process_conversation(
        "risk_calculator.py",
        sample_content,
        "conv_12345"
    )
    
    print("CAPTURE: Processed conversation")
    print(f"  Entry ID: {result['entry_id']}")
    print(f"  Graph nodes created: {len(result['graph_nodes']['insights'])} insights, "
          f"{len(result['graph_nodes']['decisions'])} decisions")
    
    # Execute decision trace query
    trace_result = eis.execute_decision_trace_query("60-day lookback")
    print("\nDECISION TRACE: Results for '60-day lookback'")
    for decision_id, trace in trace_result.items():
        print(f"  Decision: {trace['decision']['title']}")
        print(f"  Insights that led to it: {len(trace['insights'])}")
        print(f"  Files affected: {len(trace['affected_files'])}")
    
    # Generate team report
    report = eis.generate_team_intelligence_report("Engineering", "week")
    print("\nTEAM REPORT: Engineering team (last week)")
    print(f"  Key insights: {len(report['key_insights'])}")
    print(f"  Critical decisions: {len(report['critical_decisions'])}")
    
    # Unified search
    search_results = eis.search_across_systems("lookback period")
    print("\nUNIFIED SEARCH: 'lookback period'")
    print(f"  Collaboration results: {len(search_results['collaboration_results'])}")
    print(f"  Knowledge graph results: {len(search_results['knowledge_graph_results'])}")
    print(f"  Combined unique insights: {len(search_results['combined_insights'])}")
    
    # Dashboard data
    dashboard = eis.create_intelligence_dashboard_data()
    print("\nDASHBOARD DATA:")
    print(f"  System health: {dashboard['system_health']['overall']}")
    print(f"  Active users (1h): {dashboard['real_time_metrics']['active_users_1h']}")
    print(f"  Recent activity items: {len(dashboard['recent_activity'])}")
    
    print("\nSUCCESS: Enterprise Intelligence System demonstration complete")

if __name__ == "__main__":
    main()
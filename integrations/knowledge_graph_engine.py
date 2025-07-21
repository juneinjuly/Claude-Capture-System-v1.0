#!/usr/bin/env python3
"""
Knowledge Graph Engine - Intelligence Layer
Transforms conversations into a searchable knowledge graph with nodes and relationships
"""

import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
import hashlib
import uuid

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    print("WARNING: Neo4j driver not available. Install with: pip install neo4j")

class KnowledgeGraphEngine:
    """
    Intelligence Engine that creates and maintains a knowledge graph from conversations
    """
    
    def __init__(self, project_root: str = None, neo4j_uri: str = None, neo4j_user: str = None, neo4j_password: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.sqlite_db = self.project_root / "claude_capture" / "data" / "claude_auto_capture.db"
        self.graph_db = self.project_root / "claude_capture" / "data" / "claude_knowledge_graph.db"
        
        # Neo4j connection (optional)
        self.neo4j_driver = None
        if NEO4J_AVAILABLE and neo4j_uri and neo4j_user and neo4j_password:
            try:
                self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
                print("SUCCESS: Connected to Neo4j knowledge graph")
            except Exception as e:
                print(f"WARNING: Could not connect to Neo4j: {e}")
        
        # Initialize local graph database
        self.init_graph_database()
        
        # Intelligence patterns for node extraction
        self.patterns = {
            'insight': [
                r"key insight:?\s*(.+?)(?:\n|$)",
                r"important finding:?\s*(.+?)(?:\n|$)",
                r"discovered that\s*(.+?)(?:\n|$)",
                r"realized that\s*(.+?)(?:\n|$)",
                r"learned that\s*(.+?)(?:\n|$)",
                r"INSIGHT:\s*(.+?)(?:\n|$)",
                r"💡\s*(.+?)(?:\n|$)"
            ],
            'decision': [
                r"decided to\s*(.+?)(?:\n|$)",
                r"decision:\s*(.+?)(?:\n|$)",
                r"chose to\s*(.+?)(?:\n|$)",
                r"will implement\s*(.+?)(?:\n|$)",
                r"DECISION:\s*(.+?)(?:\n|$)",
                r"✅\s*(.+?)(?:\n|$)"
            ],
            'action_item': [
                r"TODO:\s*(.+?)(?:\n|$)",
                r"action item:?\s*(.+?)(?:\n|$)",
                r"need to\s*(.+?)(?:\n|$)",
                r"next step:?\s*(.+?)(?:\n|$)",
                r"should\s*(.+?)(?:\n|$)",
                r"🎯\s*(.+?)(?:\n|$)"
            ],
            'test': [
                r"test\s+(\w+)",
                r"testing\s+(.+?)(?:\n|$)",
                r"verify\s+(.+?)(?:\n|$)",
                r"check\s+(.+?)(?:\n|$)",
                r"Test.*?(\w+Algorithm)",
                r"🧪\s*(.+?)(?:\n|$)"
            ],
            'agent': [
                r"Claude\s+(suggested|recommended|implemented|created)",
                r"AI\s+(generated|created|suggested)",
                r"system\s+(detected|found|identified)",
                r"🤖\s*(.+?)(?:\n|$)"
            ]
        }
    
    def init_graph_database(self):
        """Initialize local SQLite-based graph database"""
        conn = sqlite3.connect(self.graph_db)
        cursor = conn.cursor()
        
        # Nodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                properties TEXT,
                created_at TEXT,
                updated_at TEXT,
                source_conversation_id TEXT,
                source_file_path TEXT,
                confidence REAL DEFAULT 0.0
            )
        ''')
        
        # Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                source_node_id TEXT,
                target_node_id TEXT,
                relationship_type TEXT,
                properties TEXT,
                created_at TEXT,
                confidence REAL DEFAULT 0.0,
                FOREIGN KEY (source_node_id) REFERENCES nodes (id),
                FOREIGN KEY (target_node_id) REFERENCES nodes (id)
            )
        ''')
        
        # Graph analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graph_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                metadata TEXT,
                calculated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("SUCCESS: Knowledge graph database initialized")
    
    def extract_insights_from_conversation(self, conversation_id: str, content: str, file_path: str = None) -> Dict[str, List[Dict]]:
        """Extract insights, decisions, and action items from conversation content"""
        
        extracted = {
            'insights': [],
            'decisions': [],
            'action_items': [],
            'tests': [],
            'agents': [],
            'files': []
        }
        
        # Extract insights
        for pattern in self.patterns['insight']:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                extracted['insights'].append({
                    'content': match.strip(),
                    'confidence': 0.8,
                    'source': 'pattern_match'
                })
        
        # Extract decisions
        for pattern in self.patterns['decision']:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                extracted['decisions'].append({
                    'content': match.strip(),
                    'confidence': 0.7,
                    'source': 'pattern_match'
                })
        
        # Extract action items
        for pattern in self.patterns['action_item']:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                extracted['action_items'].append({
                    'content': match.strip(),
                    'confidence': 0.6,
                    'source': 'pattern_match'
                })
        
        # Extract tests
        for pattern in self.patterns['test']:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                extracted['tests'].append({
                    'content': match.strip(),
                    'confidence': 0.5,
                    'source': 'pattern_match'
                })
        
        # Extract agent references
        for pattern in self.patterns['agent']:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                extracted['agents'].append({
                    'content': match.strip(),
                    'confidence': 0.4,
                    'source': 'pattern_match'
                })
        
        # Extract file references
        file_patterns = [
            r"([a-zA-Z0-9_]+\.py)",
            r"([a-zA-Z0-9_]+\.md)",
            r"([a-zA-Z0-9_]+\.sh)",
            r"([a-zA-Z0-9_]+\.json)"
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                extracted['files'].append({
                    'content': match.strip(),
                    'confidence': 0.9,
                    'source': 'file_reference'
                })
        
        return extracted
    
    def create_node(self, node_type: str, title: str, content: str, properties: Dict = None, 
                   source_conversation_id: str = None, source_file_path: str = None, 
                   confidence: float = 0.0) -> str:
        """Create a node in the knowledge graph"""
        
        node_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.graph_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO nodes (id, type, title, content, properties, created_at, updated_at, 
                             source_conversation_id, source_file_path, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            node_id, node_type, title, content, 
            json.dumps(properties or {}), timestamp, timestamp,
            source_conversation_id, source_file_path, confidence
        ))
        
        conn.commit()
        conn.close()
        
        # Also create in Neo4j if available
        if self.neo4j_driver:
            self.create_neo4j_node(node_id, node_type, title, content, properties, confidence)
        
        return node_id
    
    def create_relationship(self, source_node_id: str, target_node_id: str, 
                          relationship_type: str, properties: Dict = None, 
                          confidence: float = 0.0) -> str:
        """Create a relationship between two nodes"""
        
        relationship_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.graph_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO relationships (id, source_node_id, target_node_id, relationship_type, 
                                     properties, created_at, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            relationship_id, source_node_id, target_node_id, relationship_type,
            json.dumps(properties or {}), timestamp, confidence
        ))
        
        conn.commit()
        conn.close()
        
        # Also create in Neo4j if available
        if self.neo4j_driver:
            self.create_neo4j_relationship(source_node_id, target_node_id, relationship_type, properties, confidence)
        
        return relationship_id
    
    def create_neo4j_node(self, node_id: str, node_type: str, title: str, content: str, 
                         properties: Dict = None, confidence: float = 0.0):
        """Create node in Neo4j database"""
        if not self.neo4j_driver:
            return
        
        with self.neo4j_driver.session() as session:
            session.write_transaction(
                self._create_neo4j_node_tx, node_id, node_type, title, content, properties, confidence
            )
    
    def _create_neo4j_node_tx(self, tx, node_id: str, node_type: str, title: str, content: str, 
                            properties: Dict = None, confidence: float = 0.0):
        """Neo4j transaction for creating node"""
        props = properties or {}
        props.update({
            'id': node_id,
            'title': title,
            'content': content,
            'confidence': confidence,
            'created_at': datetime.now().isoformat()
        })
        
        query = f"CREATE (n:{node_type} $props)"
        tx.run(query, props=props)
    
    def create_neo4j_relationship(self, source_node_id: str, target_node_id: str, 
                                relationship_type: str, properties: Dict = None, 
                                confidence: float = 0.0):
        """Create relationship in Neo4j database"""
        if not self.neo4j_driver:
            return
        
        with self.neo4j_driver.session() as session:
            session.write_transaction(
                self._create_neo4j_relationship_tx, source_node_id, target_node_id, 
                relationship_type, properties, confidence
            )
    
    def _create_neo4j_relationship_tx(self, tx, source_node_id: str, target_node_id: str, 
                                    relationship_type: str, properties: Dict = None, 
                                    confidence: float = 0.0):
        """Neo4j transaction for creating relationship"""
        props = properties or {}
        props.update({
            'confidence': confidence,
            'created_at': datetime.now().isoformat()
        })
        
        query = f"""
        MATCH (source {{id: $source_id}})
        MATCH (target {{id: $target_id}})
        CREATE (source)-[r:{relationship_type} $props]->(target)
        """
        tx.run(query, source_id=source_node_id, target_id=target_node_id, props=props)
    
    def process_conversation_for_graph(self, conversation_id: str, content: str, 
                                     file_path: str = None, session_id: str = None) -> Dict:
        """Process a conversation and create graph nodes and relationships"""
        
        print(f"GRAPH: Processing conversation {conversation_id} for knowledge graph")
        
        # Extract insights from conversation
        extracted = self.extract_insights_from_conversation(conversation_id, content, file_path)
        
        # Create session node if provided
        session_node_id = None
        if session_id:
            session_node_id = self.create_node(
                'Session', f"Session {session_id}", f"Session {session_id}",
                {'session_id': session_id}, conversation_id, file_path, 0.9
            )
        
        # Create file node if provided
        file_node_id = None
        if file_path:
            file_node_id = self.create_node(
                'File', Path(file_path).name, file_path,
                {'file_path': file_path}, conversation_id, file_path, 1.0
            )
        
        created_nodes = {
            'session': session_node_id,
            'file': file_node_id,
            'insights': [],
            'decisions': [],
            'action_items': [],
            'tests': [],
            'agents': []
        }
        
        # Create insight nodes
        for insight in extracted['insights']:
            insight_id = self.create_node(
                'Insight', insight['content'][:50] + '...', insight['content'],
                {'source': insight['source']}, conversation_id, file_path, insight['confidence']
            )
            created_nodes['insights'].append(insight_id)
            
            # Create relationships
            if session_node_id:
                self.create_relationship(
                    insight_id, session_node_id, 'WAS_DISCUSSED_IN', {}, 0.8
                )
        
        # Create decision nodes
        for decision in extracted['decisions']:
            decision_id = self.create_node(
                'Decision', decision['content'][:50] + '...', decision['content'],
                {'source': decision['source']}, conversation_id, file_path, decision['confidence']
            )
            created_nodes['decisions'].append(decision_id)
            
            # Create relationships with insights
            for insight_id in created_nodes['insights']:
                self.create_relationship(
                    decision_id, insight_id, 'WAS_INFORMED_BY', {}, 0.7
                )
        
        # Create action item nodes
        for action_item in extracted['action_items']:
            action_id = self.create_node(
                'Action_Item', action_item['content'][:50] + '...', action_item['content'],
                {'source': action_item['source']}, conversation_id, file_path, action_item['confidence']
            )
            created_nodes['action_items'].append(action_id)
            
            # Connect to decisions
            for decision_id in created_nodes['decisions']:
                self.create_relationship(
                    action_id, decision_id, 'RESULTS_FROM', {}, 0.6
                )
        
        # Create test nodes
        for test in extracted['tests']:
            test_id = self.create_node(
                'Test', test['content'][:50] + '...', test['content'],
                {'source': test['source']}, conversation_id, file_path, test['confidence']
            )
            created_nodes['tests'].append(test_id)
            
            # Connect to session
            if session_node_id:
                self.create_relationship(
                    test_id, session_node_id, 'WAS_DESIGNED_IN', {}, 0.5
                )
        
        # Connect file modifications to session
        if file_node_id and session_node_id:
            self.create_relationship(
                file_node_id, session_node_id, 'WAS_MODIFIED_DURING', {}, 0.9
            )
        
        print(f"GRAPH: Created {len(created_nodes['insights'])} insights, {len(created_nodes['decisions'])} decisions, {len(created_nodes['action_items'])} action items")
        
        return created_nodes
    
    def query_graph(self, query_type: str, params: Dict = None) -> List[Dict]:
        """Query the knowledge graph"""
        
        if query_type == "decision_trace":
            return self.trace_decision_path(params.get('decision_id'))
        elif query_type == "session_insights":
            return self.get_session_insights(params.get('session_id'))
        elif query_type == "file_modifications":
            return self.get_file_modification_history(params.get('file_path'))
        elif query_type == "insight_network":
            return self.get_insight_network(params.get('insight_id'))
        else:
            return []
    
    def trace_decision_path(self, decision_id: str) -> List[Dict]:
        """Trace the path of insights that led to a decision"""
        conn = sqlite3.connect(self.graph_db)
        cursor = conn.cursor()
        
        # Get the decision
        cursor.execute("SELECT * FROM nodes WHERE id = ?", (decision_id,))
        decision = cursor.fetchone()
        
        if not decision:
            return []
        
        # Get all insights that informed this decision
        cursor.execute('''
            SELECT n.* FROM nodes n
            JOIN relationships r ON n.id = r.target_node_id
            WHERE r.source_node_id = ? AND r.relationship_type = 'WAS_INFORMED_BY'
        ''', (decision_id,))
        
        insights = cursor.fetchall()
        
        # Get all files modified as a result
        cursor.execute('''
            SELECT n.* FROM nodes n
            JOIN relationships r ON n.id = r.source_node_id
            WHERE r.target_node_id IN (
                SELECT r2.source_node_id FROM relationships r2
                WHERE r2.target_node_id = ? AND r2.relationship_type = 'RESULTS_FROM'
            ) AND n.type = 'File'
        ''', (decision_id,))
        
        files = cursor.fetchall()
        
        conn.close()
        
        return {
            'decision': decision,
            'insights': insights,
            'files': files
        }
    
    def get_session_insights(self, session_id: str) -> List[Dict]:
        """Get all insights from a session"""
        conn = sqlite3.connect(self.graph_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT n.* FROM nodes n
            JOIN relationships r ON n.id = r.source_node_id
            JOIN nodes s ON r.target_node_id = s.id
            WHERE s.properties LIKE ? AND r.relationship_type = 'WAS_DISCUSSED_IN'
        ''', (f'%{session_id}%',))
        
        insights = cursor.fetchall()
        conn.close()
        
        return insights
    
    def generate_graph_analytics(self) -> Dict:
        """Generate analytics about the knowledge graph"""
        conn = sqlite3.connect(self.graph_db)
        cursor = conn.cursor()
        
        # Count nodes by type
        cursor.execute('''
            SELECT type, COUNT(*) as count
            FROM nodes
            GROUP BY type
        ''')
        node_counts = dict(cursor.fetchall())
        
        # Count relationships by type
        cursor.execute('''
            SELECT relationship_type, COUNT(*) as count
            FROM relationships
            GROUP BY relationship_type
        ''')
        relationship_counts = dict(cursor.fetchall())
        
        # Get most connected nodes
        cursor.execute('''
            SELECT n.title, n.type, COUNT(r.id) as connection_count
            FROM nodes n
            LEFT JOIN relationships r ON n.id = r.source_node_id OR n.id = r.target_node_id
            GROUP BY n.id
            ORDER BY connection_count DESC
            LIMIT 10
        ''')
        most_connected = cursor.fetchall()
        
        conn.close()
        
        return {
            'node_counts': node_counts,
            'relationship_counts': relationship_counts,
            'most_connected_nodes': most_connected,
            'total_nodes': sum(node_counts.values()),
            'total_relationships': sum(relationship_counts.values())
        }
    
    def close(self):
        """Close database connections"""
        if self.neo4j_driver:
            self.neo4j_driver.close()

def main():
    """Main function for testing"""
    kg = KnowledgeGraphEngine()
    
    # Test with sample conversation
    sample_conversation = """
    Key insight: The 60-day lookback period provides the best balance between signal strength and noise reduction.
    
    Decision: We will implement a 60-day lookback for the Concentration Risk test.
    
    TODO: Modify the risk_calculator.py file to use the new lookback period.
    
    Test: We need to verify that the new lookback doesn't introduce data leakage.
    """
    
    result = kg.process_conversation_for_graph(
        "test_conv_1", sample_conversation, "risk_calculator.py", "session_123"
    )
    
    print("SUCCESS: Knowledge graph processing complete")
    print(f"NODES: Created {len(result['insights'])} insights, {len(result['decisions'])} decisions")
    
    # Generate analytics
    analytics = kg.generate_graph_analytics()
    print("ANALYTICS:", analytics)
    
    kg.close()

if __name__ == "__main__":
    main()
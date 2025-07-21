#!/usr/bin/env python3
"""
Test script for Enterprise Intelligence System
Simple validation of core functionality
"""

import sys
import os
import json
from pathlib import Path

# Add integrations to path
sys.path.insert(0, str(Path(__file__).parent.parent / "integrations"))

try:
    from enterprise_intelligence_system import EnterpriseIntelligenceSystem
    from multi_agent_collaboration import MultiAgentCollaborationFramework, UserRole
    from knowledge_graph_engine import KnowledgeGraphEngine
    print("SUCCESS: All modules imported successfully")
except ImportError as e:
    print(f"ERROR: Module import failed: {e}")
    sys.exit(1)

def test_knowledge_graph():
    """Test knowledge graph engine"""
    print("\n=== Testing Knowledge Graph Engine ===")
    
    try:
        kg = KnowledgeGraphEngine()
        
        # Test conversation processing
        sample_content = """
        Key insight: The 60-day lookback period provides optimal signal strength.
        Decision: Implement 60-day lookback across all momentum strategies.
        TODO: Update risk_calculator.py with new parameter.
        """
        
        result = kg.process_conversation_for_graph(
            "test_conv", sample_content, "risk_calculator.py", "session_test"
        )
        
        print(f"✅ Created {len(result['insights'])} insights")
        print(f"✅ Created {len(result['decisions'])} decisions") 
        print(f"✅ Created {len(result['action_items'])} action items")
        
        # Test analytics
        analytics = kg.generate_graph_analytics()
        print(f"✅ Graph analytics: {analytics['total_nodes']} nodes, {analytics['total_relationships']} relationships")
        
        return True
        
    except Exception as e:
        print(f"❌ Knowledge graph test failed: {e}")
        return False

def test_collaboration_framework():
    """Test multi-agent collaboration framework"""
    print("\n=== Testing Collaboration Framework ===")
    
    try:
        mcf = MultiAgentCollaborationFramework()
        
        # Create test users
        admin_id = mcf.create_user("test_admin", "Test Admin", "admin@test.com", UserRole.ADMIN, "Platform")
        dev_id = mcf.create_user("test_dev", "Test Dev", "dev@test.com", UserRole.DEVELOPER, "Engineering")
        
        if not admin_id or not dev_id:
            print("❌ User creation failed")
            return False
        
        print("✅ Created test users")
        
        # Create test channels
        mcf.create_default_channels(admin_id)
        print("✅ Created default channels")
        
        # Test intelligence recording
        import sqlite3
        conn = sqlite3.connect(mcf.collaboration_db)
        cursor = conn.cursor()
        cursor.execute("SELECT channel_id FROM channels WHERE channel_name = ?", ("#project-aie-core",))
        channel_result = cursor.fetchone()
        conn.close()
        
        if channel_result:
            channel_id = channel_result[0]
            entry_id = mcf.record_intelligence_entry(
                channel_id, dev_id, None, "test_entry",
                "Test insight: This is a test insight for validation.",
                "test_file.py", importance_score=0.8
            )
            print(f"✅ Recorded intelligence entry: {entry_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Collaboration framework test failed: {e}")
        return False

def test_enterprise_system():
    """Test enterprise intelligence system integration"""
    print("\n=== Testing Enterprise Intelligence System ===")
    
    try:
        eis = EnterpriseIntelligenceSystem()
        
        # Test system health
        health = eis._check_system_health()
        print(f"✅ System health check: {health['overall']}")
        
        # Test dashboard data generation
        dashboard = eis.create_intelligence_dashboard_data()
        print(f"✅ Dashboard data generated with {len(dashboard['recent_activity'])} activities")
        
        return True
        
    except Exception as e:
        print(f"❌ Enterprise system test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Enterprise Intelligence System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Knowledge Graph Engine", test_knowledge_graph),
        ("Collaboration Framework", test_collaboration_framework), 
        ("Enterprise Integration", test_enterprise_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enterprise Intelligence System is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
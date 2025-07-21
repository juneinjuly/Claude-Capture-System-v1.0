#!/usr/bin/env python3
"""
Seamless Claude Code Integration - Zero-Command Conversation Capture
Automatically captures conversations without any manual commands
"""

import os
import sys
import time
import json
import sqlite3
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import atexit
import signal
import psutil
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ClaudeCodeWatcher(FileSystemEventHandler):
    """Watches for Claude Code activity and automatically captures conversations"""
    
    def __init__(self, integration_system):
        self.integration_system = integration_system
        self.last_terminal_activity = time.time()
        self.conversation_buffer = []
        self.monitoring_active = True
        
    def on_modified(self, event):
        """Handle file modifications that might indicate Claude activity"""
        if not self.monitoring_active or event.is_directory:
            return
        
        file_path = event.src_path
        
        # Log all file activity (for debugging)
        if any(ext in file_path for ext in ['.py', '.md', '.sh', '.json']):
            timestamp = time.strftime("%H:%M:%S")
            print(f"👁️  [{timestamp}] File modified: {Path(file_path).name}")
        
        # Check if it's a potential Claude-generated file
        if self.is_claude_activity(file_path):
            print(f"🔍 [{timestamp}] Analyzing file for Claude signatures...")
            self.integration_system.process_potential_claude_activity(file_path)
        else:
            print(f"   ➡️  No Claude signatures detected")
    
    def is_claude_activity(self, file_path: str) -> bool:
        """Check if file activity suggests Claude Code interaction"""
        try:
            # Check for Claude-specific patterns
            if any(pattern in file_path for pattern in [
                'test_0', '.py', '.md', '.sh', '.json'
            ]):
                # Check file content for Claude signatures
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    claude_signatures = [
                        "from AlgorithmImports import *",
                        "class.*Test.*Algorithm",
                        "def Execute.*Analysis",
                        "SAKB Integration",
                        "Claude Code",
                        "🤖", "✅", "📊", "🎯"
                    ]
                    return any(sig in content for sig in claude_signatures)
        except:
            pass
        return False

class SeamlessClaudeIntegration:
    """
    Zero-command integration that automatically captures Claude conversations
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        
        # Integration files
        self.activity_log = self.project_root / "claude_activity.log"
        self.session_state = self.project_root / "claude_capture" / "data" / "claude_session_state.json"
        self.auto_capture_db = self.project_root / "claude_capture" / "data" / "claude_auto_capture.db"
        
        # Load or create session state
        self.session_data = self.load_session_state()
        
        # Initialize database
        self.init_auto_capture_db()
        
        # Setup monitoring
        self.watcher = ClaudeCodeWatcher(self)
        self.observer = None
        self.monitoring_thread = None
        
        # Auto-start session if needed
        self.auto_start_session()
        
        # Setup cleanup
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"🤖 Seamless Claude integration active")
        print(f"📱 Auto-capture mode: ON")
        print(f"👁️  Monitoring: {self.project_root}")
        print(f"🔍 Watching for: .py, .md, .sh, .json files")
        print(f"✨ Ready to capture Claude conversations!")
        print(f"💡 Test the system with: python3 test_capture_system.py")
    
    def load_session_state(self) -> Dict[str, Any]:
        """Load current session state"""
        if self.session_state.exists():
            try:
                with open(self.session_state, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "auto_session_active": False,
            "session_id": None,
            "session_start": None,
            "conversations_captured": 0,
            "last_activity": None
        }
    
    def save_session_state(self):
        """Save current session state"""
        with open(self.session_state, 'w') as f:
            json.dump(self.session_data, f, indent=2, default=str)
    
    def init_auto_capture_db(self):
        """Initialize auto-capture database"""
        conn = sqlite3.connect(self.auto_capture_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auto_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                conversation_type TEXT,
                activity_detected TEXT,
                file_path TEXT,
                content_sample TEXT,
                session_id TEXT,
                captured INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                activity_type TEXT,
                details TEXT,
                session_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def auto_start_session(self):
        """Automatically start a session if none is active"""
        if not self.session_data["auto_session_active"]:
            session_id = f"auto_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.session_data.update({
                "auto_session_active": True,
                "session_id": session_id,
                "session_start": datetime.now().isoformat(),
                "conversations_captured": 0,
                "last_activity": datetime.now().isoformat()
            })
            
            self.save_session_state()
            self.log_activity("session_start", f"Auto-started session {session_id}")
            
            # Start monitoring
            self.start_monitoring()
            
            print(f"🚀 Auto-session started: {session_id}")
            print(f"📱 Monitoring project directory: {self.project_root}")
            print(f"🔍 Watching for Claude Code signatures...")
            print(f"⏰ Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def start_monitoring(self):
        """Start file system monitoring"""
        if self.observer is None:
            self.observer = Observer()
            self.observer.schedule(self.watcher, str(self.project_root), recursive=True)
            self.observer.start()
            print("👁️  File monitoring started - watching for file changes...")
            print("💡 When Claude creates or modifies files, you'll see capture notifications")
    
    def stop_monitoring(self):
        """Stop file system monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("👁️  File monitoring stopped")
    
    def process_potential_claude_activity(self, file_path: str):
        """Process potential Claude Code activity"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract potential conversation elements
            conversation_indicators = self.extract_conversation_indicators(content)
            
            if conversation_indicators:
                # Store in auto-capture database
                self.store_auto_captured_activity(file_path, content, conversation_indicators)
                
                # Update session activity
                self.session_data["last_activity"] = datetime.now().isoformat()
                self.session_data["conversations_captured"] += 1
                self.save_session_state()
                
                # Enhanced logging
                timestamp = datetime.now().strftime("%H:%M:%S")
                confidence = conversation_indicators["confidence_score"]
                
                print(f"🤖 [{timestamp}] CLAUDE ACTIVITY DETECTED!")
                print(f"   📝 File: {Path(file_path).name}")
                print(f"   🎯 Confidence: {confidence:.2f}")
                print(f"   📊 Total Captured: {self.session_data['conversations_captured']}")
                
                # Log specific indicators
                if conversation_indicators.get("has_claude_signatures"):
                    print(f"   ✅ Claude signatures found")
                if conversation_indicators.get("has_implementation_code"):
                    print(f"   ✅ Implementation code detected")
                if conversation_indicators.get("has_sakb_integration"):
                    print(f"   ✅ SAKB integration detected")
                if conversation_indicators.get("has_conversation_markers"):
                    print(f"   ✅ Conversation markers found")
                
                print(f"   💾 Stored in database: claude_auto_capture.db")
                print("   " + "="*50)
                
        except Exception as e:
            print(f"⚠️  Error processing file {file_path}: {e}")  # Show errors for debugging
    
    def extract_conversation_indicators(self, content: str) -> Dict[str, Any]:
        """Extract indicators that suggest this is from a Claude conversation"""
        indicators = {
            "has_claude_signatures": False,
            "has_implementation_code": False,
            "has_sakb_integration": False,
            "has_conversation_markers": False,
            "confidence_score": 0.0
        }
        
        # Check for Claude signatures
        claude_signatures = [
            "from AlgorithmImports import *",
            "class.*Test.*Algorithm",
            "def Execute.*Analysis",
            "SAKB Integration",
            "LOG -> PROCESS -> STORE",
            "Strategic Question",
            "🤖", "✅", "📊", "🎯", "🚀"
        ]
        
        for sig in claude_signatures:
            if re.search(sig, content, re.IGNORECASE):
                indicators["has_claude_signatures"] = True
                indicators["confidence_score"] += 0.2
                break
        
        # Check for implementation patterns
        implementation_patterns = [
            r"def initialize_indicators\(",
            r"def execute_.*_analysis\(",
            r"def OnData\(",
            r"class.*Framework.*Algorithm",
            r"self\.Log\("
        ]
        
        for pattern in implementation_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                indicators["has_implementation_code"] = True
                indicators["confidence_score"] += 0.3
                break
        
        # Check for SAKB integration
        sakb_patterns = [
            "SAKB Integration",
            "LOG.*PROCESS.*STORE",
            "Tier 1.*Tier 2.*Tier 3",
            "Strategic.*Knowledge.*Base"
        ]
        
        for pattern in sakb_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                indicators["has_sakb_integration"] = True
                indicators["confidence_score"] += 0.3
                break
        
        # Check for conversation markers
        conversation_markers = [
            "# region imports",
            "\"\"\".*TEST.*\"\"\"",
            "CRITICAL:",
            "IMPORTANT:",
            "Strategic Question"
        ]
        
        for marker in conversation_markers:
            if re.search(marker, content, re.IGNORECASE):
                indicators["has_conversation_markers"] = True
                indicators["confidence_score"] += 0.2
                break
        
        return indicators if indicators["confidence_score"] > 0.3 else None
    
    def store_auto_captured_activity(self, file_path: str, content: str, indicators: Dict[str, Any]):
        """Store auto-captured activity in database"""
        conn = sqlite3.connect(self.auto_capture_db)
        cursor = conn.cursor()
        
        # Create content sample (first 200 chars)
        content_sample = content[:200] + "..." if len(content) > 200 else content
        
        cursor.execute('''
            INSERT INTO auto_conversations (
                timestamp, conversation_type, activity_detected, file_path, 
                content_sample, session_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            "file_modification",
            json.dumps(indicators),
            file_path,
            content_sample,
            self.session_data["session_id"]
        ))
        
        conn.commit()
        conn.close()
    
    def log_activity(self, activity_type: str, details: str):
        """Log activity to database"""
        conn = sqlite3.connect(self.auto_capture_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_log (timestamp, activity_type, details, session_id)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            activity_type,
            details,
            self.session_data["session_id"]
        ))
        
        conn.commit()
        conn.close()
    
    def get_activity_summary(self) -> Dict[str, Any]:
        """Get summary of auto-captured activity"""
        conn = sqlite3.connect(self.auto_capture_db)
        cursor = conn.cursor()
        
        # Get conversation count
        cursor.execute('''
            SELECT COUNT(*) FROM auto_conversations 
            WHERE session_id = ?
        ''', (self.session_data["session_id"],))
        
        conversation_count = cursor.fetchone()[0]
        
        # Get recent activity
        cursor.execute('''
            SELECT timestamp, activity_type, details FROM activity_log
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (self.session_data["session_id"],))
        
        recent_activity = cursor.fetchall()
        
        conn.close()
        
        return {
            "session_id": self.session_data["session_id"],
            "session_start": self.session_data["session_start"],
            "conversations_captured": conversation_count,
            "last_activity": self.session_data["last_activity"],
            "recent_activity": recent_activity
        }
    
    def integrate_with_existing_system(self):
        """Integrate captured conversations with existing Claude system"""
        try:
            # Import existing integration system
            from claude_code_integration import ClaudeCodeIntegrationSystem
            
            ccis = ClaudeCodeIntegrationSystem(self.project_root)
            
            # Get unprocessed conversations
            conn = sqlite3.connect(self.auto_capture_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM auto_conversations 
                WHERE captured = 0 AND session_id = ?
            ''', (self.session_data["session_id"],))
            
            unprocessed = cursor.fetchall()
            
            # Process each conversation
            for conv in unprocessed:
                conv_id, timestamp, conv_type, activity, file_path, content, session_id, captured = conv
                
                # Create a pseudo-conversation for the system
                user_input = f"Auto-detected Claude activity in {Path(file_path).name}"
                claude_response = content[:1000] + "..." if len(content) > 1000 else content
                
                # Capture in main system
                ccis.capture_claude_conversation(
                    user_input=user_input,
                    claude_response=claude_response,
                    tools_used=["Write", "Edit", "MultiEdit"],
                    auto_analyze=True
                )
                
                # Mark as processed
                cursor.execute('''
                    UPDATE auto_conversations 
                    SET captured = 1 
                    WHERE id = ?
                ''', (conv_id,))
            
            conn.commit()
            conn.close()
            
            print(f"📊 Integrated {len(unprocessed)} auto-captured conversations")
            
        except ImportError:
            print("⚠️  Main Claude integration system not available")
        except Exception as e:
            print(f"⚠️  Integration error: {e}")
    
    def cleanup(self):
        """Cleanup when shutting down"""
        if self.session_data["auto_session_active"]:
            self.stop_monitoring()
            self.integrate_with_existing_system()
            
            # Update session state
            self.session_data["auto_session_active"] = False
            self.save_session_state()
            
            print("🏁 Seamless Claude integration ended")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.cleanup()
        sys.exit(0)


def main():
    """Main function to start seamless integration"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Seamless Claude Code Integration")
    parser.add_argument("--start", action="store_true", help="Start seamless monitoring")
    parser.add_argument("--stop", action="store_true", help="Stop seamless monitoring")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--integrate", action="store_true", help="Integrate with main system")
    
    args = parser.parse_args()
    
    sci = SeamlessClaudeIntegration()
    
    if args.stop:
        sci.cleanup()
    elif args.status:
        summary = sci.get_activity_summary()
        print(json.dumps(summary, indent=2))
    elif args.integrate:
        sci.integrate_with_existing_system()
    elif args.start:
        print("🚀 Starting seamless Claude integration...")
        print("👁️  Monitoring for Claude activity...")
        print("📱 Auto-capture mode: ACTIVE")
        print("⏹️  Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            sci.cleanup()
    else:
        # Default: show status and start if needed
        summary = sci.get_activity_summary()
        print("🤖 Seamless Claude Integration Status:")
        print(f"📊 Session: {summary['session_id']}")
        print(f"📊 Conversations: {summary['conversations_captured']}")
        print(f"📊 Last Activity: {summary['last_activity']}")
        print()
        print("💡 The system is automatically monitoring for Claude activity")
        print("💡 No manual commands needed - just use Claude normally!")


if __name__ == "__main__":
    main()
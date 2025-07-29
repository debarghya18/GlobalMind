#!/usr/bin/env python3
"""
Simple database test script for GlobalMind
Tests basic database functionality
"""

import asyncio
import sqlite3
import os
from datetime import datetime
from pathlib import Path

async def create_database():
    """Create and test the database"""
    print("🔧 Creating GlobalMind Database...")
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    db_path = data_dir / "globalmind.db"
    
    # Create SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anonymous_id TEXT UNIQUE NOT NULL,
                language_preference TEXT,
                cultural_background TEXT,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                anonymous_user_id TEXT,
                language TEXT,
                cultural_context TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                mood_score REAL,
                crisis_detected BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (anonymous_user_id) REFERENCES users(anonymous_id)
            )
        """)
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_type TEXT,
                content_encrypted TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT,
                sentiment_score REAL,
                crisis_level REAL DEFAULT 0.0,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Create progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anonymous_user_id TEXT,
                date DATE,
                mood_score REAL,
                session_count INTEGER DEFAULT 0,
                crisis_incidents INTEGER DEFAULT 0,
                satisfaction_rating REAL,
                notes_encrypted TEXT,
                FOREIGN KEY (anonymous_user_id) REFERENCES users(anonymous_id)
            )
        """)
        
        # Create feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anonymous_user_id TEXT,
                session_id TEXT,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                comment_encrypted TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (anonymous_user_id) REFERENCES users(anonymous_id),
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Create system metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                additional_data TEXT
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_anonymous_id ON users(anonymous_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(anonymous_user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_progress_user_date ON progress(anonymous_user_id, date)")
        
        # Commit changes
        conn.commit()
        print("✅ Database tables created successfully!")
        
        # Insert sample data
        cursor.execute("""
            INSERT INTO users (anonymous_id, language_preference, cultural_background, preferences)
            VALUES (?, ?, ?, ?)
        """, ("anon_user_001", "en", "western", "{}"))
        
        cursor.execute("""
            INSERT INTO sessions (session_id, anonymous_user_id, language, cultural_context)
            VALUES (?, ?, ?, ?)
        """, ("session_001", "anon_user_001", "en", "{}"))
        
        cursor.execute("""
            INSERT INTO conversations (session_id, message_type, content_encrypted, language, sentiment_score)
            VALUES (?, ?, ?, ?, ?)
        """, ("session_001", "user", "Hello, I'm feeling anxious today.", "en", 0.3))
        
        cursor.execute("""
            INSERT INTO progress (anonymous_user_id, date, mood_score, session_count)
            VALUES (?, ?, ?, ?)
        """, ("anon_user_001", datetime.now().date(), 4.0, 1))
        
        cursor.execute("""
            INSERT INTO feedback (anonymous_user_id, session_id, rating, comment_encrypted)
            VALUES (?, ?, ?, ?)
        """, ("anon_user_001", "session_001", 5, "Very helpful session!"))
        
        cursor.execute("""
            INSERT INTO system_metrics (metric_name, metric_value, additional_data)
            VALUES (?, ?, ?)
        """, ("anxiety_level", 3.5, "{}"))
        
        conn.commit()
        print("✅ Sample data inserted successfully!")
        
        # Test queries
        print("\n📊 Testing Database Queries...")
        
        # Count users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Users: {user_count}")
        
        # Count sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        session_count = cursor.fetchone()[0]
        print(f"✅ Sessions: {session_count}")
        
        # Count conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conversation_count = cursor.fetchone()[0]
        print(f"✅ Conversations: {conversation_count}")
        
        # Count progress entries
        cursor.execute("SELECT COUNT(*) FROM progress")
        progress_count = cursor.fetchone()[0]
        print(f"✅ Progress entries: {progress_count}")
        
        # Count feedback entries
        cursor.execute("SELECT COUNT(*) FROM feedback")
        feedback_count = cursor.fetchone()[0]
        print(f"✅ Feedback entries: {feedback_count}")
        
        # Count system metrics
        cursor.execute("SELECT COUNT(*) FROM system_metrics")
        metrics_count = cursor.fetchone()[0]
        print(f"✅ System metrics: {metrics_count}")
        
        # Get user progress
        cursor.execute("""
            SELECT date, mood_score, session_count 
            FROM progress 
            WHERE anonymous_user_id = ? 
            ORDER BY date DESC
        """, ("anon_user_001",))
        
        progress_data = cursor.fetchall()
        print(f"✅ Retrieved {len(progress_data)} progress records")
        
        # Get session data
        cursor.execute("""
            SELECT session_id, language, started_at, total_messages, crisis_detected
            FROM sessions 
            WHERE anonymous_user_id = ?
        """, ("anon_user_001",))
        
        session_data = cursor.fetchall()
        print(f"✅ Retrieved {len(session_data)} session records")
        
        print("\n🎉 Database test completed successfully!")
        print(f"📁 Database file: {db_path}")
        print(f"💾 Database size: {os.path.getsize(db_path)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        conn.close()
        print("✅ Database connection closed")

if __name__ == "__main__":
    print("🚀 GlobalMind Database Test")
    print("=" * 40)
    
    success = asyncio.run(create_database())
    
    if success:
        print("\n✅ Database test passed! Ready for use.")
    else:
        print("\n❌ Database test failed!")

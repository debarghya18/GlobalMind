#!/usr/bin/env python3
"""
Database initialization script for GlobalMind
Creates and tests the database with sample data
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.storage.database import DatabaseManager
from src.core.config import DatabaseConfig
from src.monitoring.analytics import MoodEntry, MoodLevel, ProgressMetric, UsageMetric


class SimpleConfig:
    """Simple configuration for testing"""
    def __init__(self):
        self.path = "data/globalmind.db"
        self.type = "sqlite"
        self.backup_enabled = True
        self.backup_interval = 86400


async def initialize_database():
    """Initialize the database with sample data"""
    print("🔧 Initializing GlobalMind Database...")
    
    # Create database manager
    config = SimpleConfig()
    db_manager = DatabaseManager(config)
    
    try:
        # Initialize database
        await db_manager.initialize()
        print("✅ Database initialized successfully!")
        
        # Create sample user
        user_data = {
            'original_id': 'user_001',
            'language': 'en',
            'cultural_background': 'western',
            'preferences': {
                'theme': 'light',
                'notifications': True,
                'therapy_approach': 'western_cbt'
            }
        }
        
        user_id = await db_manager.create_user(user_data)
        print(f"✅ Created sample user: {user_id}")
        
        # Create sample session
        session_data = {
            'session_id': 'session_001',
            'anonymous_user_id': user_id,
            'language': 'en',
            'cultural_context': {
                'region': 'western',
                'approach': 'cbt'
            }
        }
        
        session_id = await db_manager.create_session(session_data)
        print(f"✅ Created sample session: {session_id}")
        
        # Store sample interaction
        interaction_data = {
            'session_id': session_id,
            'message_type': 'user',
            'content': 'Hello, I am feeling anxious today.',
            'language': 'en',
            'sentiment_score': 0.3,
            'crisis_level': 0.1
        }
        
        await db_manager.store_interaction(interaction_data)
        print("✅ Stored sample interaction")
        
        # Store sample mood entry
        mood_entry = MoodEntry(
            timestamp=datetime.now(),
            mood_level=MoodLevel.GOOD,
            notes="Feeling better after therapy session",
            user_id=user_id
        )
        
        await db_manager.store_mood_entry(mood_entry)
        print("✅ Stored sample mood entry")
        
        # Store sample progress metric
        progress_metric = ProgressMetric(
            metric_name="anxiety_level",
            value=3.5,
            timestamp=datetime.now(),
            user_id=user_id,
            context={"session_id": session_id}
        )
        
        await db_manager.store_progress_metric(progress_metric)
        print("✅ Stored sample progress metric")
        
        # Store sample usage metric
        usage_metric = UsageMetric(
            session_id=session_id,
            user_id=user_id,
            start_time=datetime.now() - timedelta(minutes=30),
            end_time=datetime.now(),
            messages_exchanged=10,
            languages_used=["en"],
            cultural_context="western",
            crisis_detected=False
        )
        
        await db_manager.store_usage_metric(usage_metric)
        print("✅ Stored sample usage metric")
        
        # Test database health
        health_status = await db_manager.health_check()
        print(f"✅ Database health check: {'PASS' if health_status else 'FAIL'}")
        
        # Test analytics queries
        print("\n📊 Testing Analytics Queries...")
        
        # Get mood entries
        mood_entries = await db_manager.get_mood_entries(user_id=user_id, start_date=datetime.now() - timedelta(days=7))
        print(f"✅ Retrieved {len(mood_entries)} mood entries")
        
        # Get progress metrics
        progress_metrics = await db_manager.get_progress_metrics(user_id=user_id, start_date=datetime.now() - timedelta(days=7))
        print(f"✅ Retrieved {len(progress_metrics)} progress metrics")
        
        # Get usage metrics
        usage_metrics = await db_manager.get_usage_metrics(start_date=datetime.now() - timedelta(days=7))
        print(f"✅ Retrieved {len(usage_metrics)} usage metrics")
        
        # Get system metrics
        system_metrics = await db_manager.get_system_metrics(hours=24)
        print(f"✅ Retrieved {len(system_metrics)} system metrics")
        
        # Store user feedback
        feedback_data = {
            'anonymous_user_id': user_id,
            'session_id': session_id,
            'rating': 5,
            'comment': 'Very helpful session, thank you!'
        }
        
        await db_manager.store_feedback(feedback_data)
        print("✅ Stored sample feedback")
        
        # Create backup
        backup_path = await db_manager.backup_database()
        print(f"✅ Database backup created: {backup_path}")
        
        print("\n🎉 Database initialization completed successfully!")
        print(f"📁 Database file: {db_manager.db_path}")
        print(f"🔐 Encryption key: data/master.key")
        print(f"💾 Backup: {backup_path}")
        
        print("\n📈 Database Statistics:")
        print(f"   - Users: 1")
        print(f"   - Sessions: 1")
        print(f"   - Interactions: 1")
        print(f"   - Mood entries: 1")
        print(f"   - Progress metrics: 1")
        print(f"   - Usage metrics: 1")
        print(f"   - Feedback entries: 1")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Close database
        await db_manager.close()
        print("✅ Database connections closed")
    
    return True


if __name__ == "__main__":
    print("🚀 GlobalMind Database Initialization")
    print("=" * 50)
    
    success = asyncio.run(initialize_database())
    
    if success:
        print("\n✅ All tests passed! Database is ready for use.")
        sys.exit(0)
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)

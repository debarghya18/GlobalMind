"""
Database manager for GlobalMind
Handles encrypted data storage with privacy compliance
"""

import asyncio
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
import aiosqlite
from pathlib import Path

from ..core.config import DatabaseConfig
from ..core.exceptions import DatabaseError, PrivacyError
from ..security.encryption import EncryptionManager


class DatabaseManager:
    """Manages database operations with encryption and privacy"""
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize database manager
        
        Args:
            config: Database configuration
        """
        self.config = config
        self.db_path = Path(config.path)
        self.encryption_manager = None
        self.connection_pool = {}
        
        # Ensure data directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Database manager initialized with path: {self.db_path}")
    
    async def initialize(self):
        """Initialize database and create tables"""
        try:
            # Initialize encryption if not already done
            if not self.encryption_manager:
                from ..security.encryption import EncryptionManager
                from ..core.config import SecurityConfig
                
                # Create a basic security config for encryption
                security_config = SecurityConfig(
                    encryption_algorithm="AES-256-GCM",
                    key_rotation_days=30,
                    anonymize_data=True,
                    data_retention_days=365,
                    gdpr_compliance=True,
                    hipaa_compliance=True,
                    delete_on_request=True,
                    session_timeout=3600,
                    max_sessions=3,
                    require_2fa=False
                )
                self.encryption_manager = EncryptionManager(security_config)
            
            # Create database tables
            await self._create_tables()
            
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise DatabaseError(f"Database initialization failed: {e}", "DB_001")
    
    async def _create_tables(self):
        """Create database tables"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Users table (anonymized)
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anonymous_id TEXT UNIQUE NOT NULL,
                        language_preference TEXT,
                        cultural_background TEXT,
                        preferences TEXT,  -- Encrypted JSON
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Sessions table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        anonymous_user_id TEXT,
                        language TEXT,
                        cultural_context TEXT,  -- Encrypted JSON
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ended_at TIMESTAMP,
                        total_messages INTEGER DEFAULT 0,
                        mood_score REAL,
                        crisis_detected BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (anonymous_user_id) REFERENCES users(anonymous_id)
                    )
                """)
                
                # Conversations table (encrypted)
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        message_type TEXT,  -- 'user' or 'assistant'
                        content_encrypted TEXT,  -- Encrypted message content
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        language TEXT,
                        sentiment_score REAL,
                        crisis_level REAL DEFAULT 0.0,
                        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                    )
                """)
                
                # Progress tracking table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anonymous_user_id TEXT,
                        date DATE,
                        mood_score REAL,
                        session_count INTEGER DEFAULT 0,
                        crisis_incidents INTEGER DEFAULT 0,
                        satisfaction_rating REAL,
                        notes_encrypted TEXT,  -- Encrypted notes
                        FOREIGN KEY (anonymous_user_id) REFERENCES users(anonymous_id)
                    )
                """)
                
                # Feedback table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anonymous_user_id TEXT,
                        session_id TEXT,
                        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                        comment_encrypted TEXT,  -- Encrypted comment
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (anonymous_user_id) REFERENCES users(anonymous_id),
                        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                    )
                """)
                
                # System metrics table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS system_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metric_name TEXT,
                        metric_value REAL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        additional_data TEXT  -- JSON data
                    )
                """)
                
                # Create indexes for performance
                await db.execute("CREATE INDEX IF NOT EXISTS idx_users_anonymous_id ON users(anonymous_id)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(anonymous_user_id)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_progress_user_date ON progress(anonymous_user_id, date)")
                
                await db.commit()
                
                logger.info("Database tables created successfully")
                
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise DatabaseError(f"Table creation failed: {e}", "DB_003")
    
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """
        Create a new anonymous user
        
        Args:
            user_data: User data dictionary
            
        Returns:
            str: Anonymous user ID
        """
        try:
            # Generate anonymous ID
            anonymous_id = self.encryption_manager.anonymize_user_id(
                user_data.get('original_id', f"user_{datetime.now().timestamp()}")
            )
            
            # Encrypt preferences
            preferences_encrypted = self.encryption_manager.encrypt_json(
                user_data.get('preferences', {})
            )
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO users (anonymous_id, language_preference, cultural_background, preferences)
                    VALUES (?, ?, ?, ?)
                """, (
                    anonymous_id,
                    user_data.get('language', 'en'),
                    user_data.get('cultural_background', 'western'),
                    preferences_encrypted
                ))
                
                await db.commit()
                
                logger.info(f"Created anonymous user: {anonymous_id}")
                return anonymous_id
                
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise DatabaseError(f"User creation failed: {e}", "DB_002")
    
    async def create_session(self, session_data: Dict[str, Any]) -> str:
        """
        Create a new session
        
        Args:
            session_data: Session data
            
        Returns:
            str: Session ID
        """
        try:
            session_id = session_data.get('session_id', f"session_{datetime.now().timestamp()}")
            
            # Encrypt cultural context
            cultural_context_encrypted = self.encryption_manager.encrypt_json(
                session_data.get('cultural_context', {})
            )
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO sessions (session_id, anonymous_user_id, language, cultural_context)
                    VALUES (?, ?, ?, ?)
                """, (
                    session_id,
                    session_data.get('anonymous_user_id'),
                    session_data.get('language', 'en'),
                    cultural_context_encrypted
                ))
                
                await db.commit()
                
                logger.info(f"Created session: {session_id}")
                return session_id
                
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise DatabaseError(f"Session creation failed: {e}", "DB_002")
    
    async def store_interaction(self, interaction_data: Dict[str, Any]):
        """
        Store encrypted user interaction
        
        Args:
            interaction_data: Interaction data to store
        """
        try:
            # Encrypt message content
            content_encrypted = self.encryption_manager.encrypt_data(
                interaction_data.get('content', '')
            )
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO conversations 
                    (session_id, message_type, content_encrypted, language, sentiment_score, crisis_level)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    interaction_data.get('session_id'),
                    interaction_data.get('message_type', 'user'),
                    content_encrypted,
                    interaction_data.get('language', 'en'),
                    interaction_data.get('sentiment_score', 0.0),
                    interaction_data.get('crisis_level', 0.0)
                ))
                
                await db.commit()
                
                logger.debug("Stored encrypted interaction")
                
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")
            raise DatabaseError(f"Interaction storage failed: {e}", "DB_002")
    
    async def get_user_progress(self, anonymous_user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get user progress data
        
        Args:
            anonymous_user_id: Anonymous user ID
            days: Number of days to retrieve
            
        Returns:
            List of progress data
        """
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("""
                    SELECT date, mood_score, session_count, satisfaction_rating
                    FROM progress 
                    WHERE anonymous_user_id = ? AND date >= ?
                    ORDER BY date
                """, (anonymous_user_id, start_date.date())) as cursor:
                    
                    rows = await cursor.fetchall()
                    
                    progress_data = []
                    for row in rows:
                        progress_data.append({
                            'date': row[0],
                            'mood_score': row[1],
                            'session_count': row[2],
                            'satisfaction_rating': row[3]
                        })
                    
                    return progress_data
                    
        except Exception as e:
            logger.error(f"Failed to get user progress: {e}")
            raise DatabaseError(f"Progress retrieval failed: {e}", "DB_002")
    
    async def update_user_progress(self, progress_data: Dict[str, Any]):
        """
        Update user progress data
        
        Args:
            progress_data: Progress data to update
        """
        try:
            # Encrypt notes if present
            notes_encrypted = None
            if progress_data.get('notes'):
                notes_encrypted = self.encryption_manager.encrypt_data(progress_data['notes'])
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO progress 
                    (anonymous_user_id, date, mood_score, session_count, 
                     crisis_incidents, satisfaction_rating, notes_encrypted)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    progress_data['anonymous_user_id'],
                    progress_data.get('date', datetime.now().date()),
                    progress_data.get('mood_score'),
                    progress_data.get('session_count', 0),
                    progress_data.get('crisis_incidents', 0),
                    progress_data.get('satisfaction_rating'),
                    notes_encrypted
                ))
                
                await db.commit()
                
                logger.debug("Updated user progress")
                
        except Exception as e:
            logger.error(f"Failed to update progress: {e}")
            raise DatabaseError(f"Progress update failed: {e}", "DB_002")
    
    async def store_feedback(self, feedback_data: Dict[str, Any]):
        """
        Store user feedback
        
        Args:
            feedback_data: Feedback data
        """
        try:
            # Encrypt comment
            comment_encrypted = None
            if feedback_data.get('comment'):
                comment_encrypted = self.encryption_manager.encrypt_data(feedback_data['comment'])
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO feedback (anonymous_user_id, session_id, rating, comment_encrypted)
                    VALUES (?, ?, ?, ?)
                """, (
                    feedback_data.get('anonymous_user_id'),
                    feedback_data.get('session_id'),
                    feedback_data.get('rating'),
                    comment_encrypted
                ))
                
                await db.commit()
                
                logger.info("Stored user feedback")
                
        except Exception as e:
            logger.error(f"Failed to store feedback: {e}")
            raise DatabaseError(f"Feedback storage failed: {e}", "DB_002")
    
    async def get_system_metrics(self, metric_name: str = None, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get system metrics
        
        Args:
            metric_name: Specific metric name (optional)
            hours: Number of hours to retrieve
            
        Returns:
            List of metrics
        """
        try:
            start_time = datetime.now() - timedelta(hours=hours)
            
            query = """
                SELECT metric_name, metric_value, timestamp, additional_data
                FROM system_metrics 
                WHERE timestamp >= ?
            """
            params = [start_time]
            
            if metric_name:
                query += " AND metric_name = ?"
                params.append(metric_name)
            
            query += " ORDER BY timestamp"
            
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    
                    metrics = []
                    for row in rows:
                        metric = {
                            'metric_name': row[0],
                            'metric_value': row[1],
                            'timestamp': row[2],
                        }
                        
                        if row[3]:
                            try:
                                metric['additional_data'] = json.loads(row[3])
                            except json.JSONDecodeError:
                                metric['additional_data'] = {}
                        
                        metrics.append(metric)
                    
                    return metrics
                    
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            raise DatabaseError(f"Metrics retrieval failed: {e}", "DB_002")
    
    async def store_system_metric(self, metric_name: str, metric_value: float, additional_data: Dict[str, Any] = None):
        """
        Store system metric
        
        Args:
            metric_name: Name of the metric
            metric_value: Metric value
            additional_data: Additional data (optional)
        """
        try:
            additional_json = json.dumps(additional_data) if additional_data else None
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO system_metrics (metric_name, metric_value, additional_data)
                    VALUES (?, ?, ?)
                """, (metric_name, metric_value, additional_json))
                
                await db.commit()
                
        except Exception as e:
            logger.error(f"Failed to store system metric: {e}")
            raise DatabaseError(f"Metric storage failed: {e}", "DB_002")
    
    async def delete_user_data(self, anonymous_user_id: str):
        """
        Delete all user data (GDPR compliance)
        
        Args:
            anonymous_user_id: Anonymous user ID
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Get all sessions for this user
                async with db.execute("""
                    SELECT session_id FROM sessions WHERE anonymous_user_id = ?
                """, (anonymous_user_id,)) as cursor:
                    sessions = await cursor.fetchall()
                    session_ids = [row[0] for row in sessions]
                
                # Delete conversations
                for session_id in session_ids:
                    await db.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
                
                # Delete sessions
                await db.execute("DELETE FROM sessions WHERE anonymous_user_id = ?", (anonymous_user_id,))
                
                # Delete progress
                await db.execute("DELETE FROM progress WHERE anonymous_user_id = ?", (anonymous_user_id,))
                
                # Delete feedback
                await db.execute("DELETE FROM feedback WHERE anonymous_user_id = ?", (anonymous_user_id,))
                
                # Delete user
                await db.execute("DELETE FROM users WHERE anonymous_id = ?", (anonymous_user_id,))
                
                await db.commit()
                
                logger.info(f"Deleted all data for user: {anonymous_user_id}")
                
        except Exception as e:
            logger.error(f"Failed to delete user data: {e}")
            raise PrivacyError(f"Data deletion failed: {e}", "PRIVACY_003")
    
    async def cleanup_old_data(self, days: int):
        """
        Cleanup old data based on retention policy
        
        Args:
            days: Number of days to retain data
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            async with aiosqlite.connect(self.db_path) as db:
                # Delete old conversations
                await db.execute("""
                    DELETE FROM conversations WHERE timestamp < ?
                """, (cutoff_date,))
                
                # Delete old sessions
                await db.execute("""
                    DELETE FROM sessions WHERE started_at < ?
                """, (cutoff_date,))
                
                # Delete old metrics
                await db.execute("""
                    DELETE FROM system_metrics WHERE timestamp < ?
                """, (cutoff_date,))
                
                await db.commit()
                
                logger.info(f"Cleaned up data older than {cutoff_date}")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            raise DatabaseError(f"Data cleanup failed: {e}", "DB_002")
    
    async def health_check(self) -> bool:
        """
        Perform database health check
        
        Returns:
            bool: True if healthy
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("SELECT 1")
                return True
                
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def close(self):
        """Close database connections"""
        try:
            # Close any open connections
            self.connection_pool.clear()
            logger.info("Database connections closed")
            
        except Exception as e:
            logger.error(f"Error closing database: {e}")
    
    async def backup_database(self):
        """Create database backup"""
        try:
            backup_path = self.db_path.parent / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            async with aiosqlite.connect(self.db_path) as source:
                async with aiosqlite.connect(backup_path) as backup:
                    await source.backup(backup)
            
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            raise DatabaseError(f"Backup failed: {e}", "DB_003")
    
    # Analytics support methods
    async def store_mood_entry(self, mood_entry):
        """Store mood entry for analytics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO progress (anonymous_user_id, date, mood_score, notes_encrypted)
                    VALUES (?, ?, ?, ?)
                """, (
                    mood_entry.user_id or 'anonymous',
                    mood_entry.timestamp.date(),
                    mood_entry.mood_level.value,
                    self.encryption_manager.encrypt_data(mood_entry.notes or '')
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to store mood entry: {e}")
            raise DatabaseError(f"Mood entry storage failed: {e}", "DB_002")
    
    async def store_progress_metric(self, progress_metric):
        """Store progress metric for analytics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO system_metrics (metric_name, metric_value, additional_data)
                    VALUES (?, ?, ?)
                """, (
                    progress_metric.metric_name,
                    progress_metric.value,
                    json.dumps({
                        'user_id': progress_metric.user_id,
                        'timestamp': progress_metric.timestamp.isoformat(),
                        'context': progress_metric.context
                    })
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to store progress metric: {e}")
            raise DatabaseError(f"Progress metric storage failed: {e}", "DB_002")
    
    async def store_usage_metric(self, usage_metric):
        """Store usage metric for analytics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO sessions (session_id, anonymous_user_id, language, started_at, ended_at, total_messages, crisis_detected)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    usage_metric.session_id,
                    usage_metric.user_id or 'anonymous',
                    usage_metric.languages_used[0] if usage_metric.languages_used else 'en',
                    usage_metric.start_time,
                    usage_metric.end_time,
                    usage_metric.messages_exchanged,
                    usage_metric.crisis_detected
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to store usage metric: {e}")
            raise DatabaseError(f"Usage metric storage failed: {e}", "DB_002")
    
    async def get_mood_entries(self, user_id=None, start_date=None, end_date=None):
        """Get mood entries for analytics"""
        try:
            query = "SELECT * FROM progress WHERE 1=1"
            params = []
            
            if user_id:
                query += " AND anonymous_user_id = ?"
                params.append(user_id)
            if start_date:
                query += " AND date >= ?"
                params.append(start_date.date())
            if end_date:
                query += " AND date <= ?"
                params.append(end_date.date())
            
            query += " ORDER BY date"
            
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    
                    # Convert to mock mood entries for analytics
                    from ..monitoring.analytics import MoodEntry, MoodLevel
                    mood_entries = []
                    for row in rows:
                        if row[2]:  # mood_score exists
                            mood_entries.append(MoodEntry(
                                timestamp=datetime.fromisoformat(str(row[1])),
                                mood_level=MoodLevel(int(row[2])),
                                notes=self.encryption_manager.decrypt_data(row[6]).decode() if row[6] else None,
                                user_id=row[0]
                            ))
                    
                    return mood_entries
        except Exception as e:
            logger.error(f"Failed to get mood entries: {e}")
            return []
    
    async def get_progress_metrics(self, user_id=None, start_date=None, end_date=None):
        """Get progress metrics for analytics"""
        try:
            query = "SELECT * FROM system_metrics WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)
            
            query += " ORDER BY timestamp"
            
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    
                    # Convert to mock progress metrics
                    from ..monitoring.analytics import ProgressMetric
                    progress_metrics = []
                    for row in rows:
                        additional_data = json.loads(row[4]) if row[4] else {}
                        if additional_data.get('user_id') == user_id or user_id is None:
                            progress_metrics.append(ProgressMetric(
                                metric_name=row[1],
                                value=row[2],
                                timestamp=datetime.fromisoformat(row[3]),
                                user_id=additional_data.get('user_id'),
                                context=additional_data.get('context')
                            ))
                    
                    return progress_metrics
        except Exception as e:
            logger.error(f"Failed to get progress metrics: {e}")
            return []
    
    async def get_usage_metrics(self, start_date=None, end_date=None):
        """Get usage metrics for analytics"""
        try:
            query = "SELECT * FROM sessions WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND started_at >= ?"
                params.append(start_date)
            if end_date:
                query += " AND started_at <= ?"
                params.append(end_date)
            
            query += " ORDER BY started_at"
            
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    
                    # Convert to mock usage metrics
                    from ..monitoring.analytics import UsageMetric
                    usage_metrics = []
                    for row in rows:
                        usage_metrics.append(UsageMetric(
                            session_id=row[1],
                            user_id=row[2],
                            start_time=datetime.fromisoformat(row[5]),
                            end_time=datetime.fromisoformat(row[6]) if row[6] else None,
                            messages_exchanged=row[7] or 0,
                            languages_used=[row[3]] if row[3] else ['en'],
                            cultural_context=row[4],
                            crisis_detected=bool(row[9])
                        ))
                    
                    return usage_metrics
        except Exception as e:
            logger.error(f"Failed to get usage metrics: {e}")
            return []
    
    async def get_crisis_events(self, start_date=None, end_date=None):
        """Get crisis events for analytics"""
        try:
            query = "SELECT * FROM sessions WHERE crisis_detected = 1"
            params = []
            
            if start_date:
                query += " AND started_at >= ?"
                params.append(start_date)
            if end_date:
                query += " AND started_at <= ?"
                params.append(end_date)
            
            query += " ORDER BY started_at"
            
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    
                    # Convert to crisis events
                    crisis_events = []
                    for row in rows:
                        crisis_events.append({
                            'session_id': row[1],
                            'user_id': row[2],
                            'timestamp': datetime.fromisoformat(row[5]),
                            'cultural_context': row[4],
                            'severity': 'high'  # Default severity
                        })
                    
                    return crisis_events
        except Exception as e:
            logger.error(f"Failed to get crisis events: {e}")
            return []

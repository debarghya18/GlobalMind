"""
Meditation system for GlobalMind
Provides culturally-diverse meditation practices and guided sessions
"""

import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from enum import Enum
import random

from ..core.exceptions import ModelError


class MeditationType(Enum):
    """Types of meditation practices"""
    MINDFULNESS = "mindfulness"
    BREATHING = "breathing"
    BODY_SCAN = "body_scan"
    LOVING_KINDNESS = "loving_kindness"
    WALKING = "walking"
    MANTRA = "mantra"
    VISUALIZATION = "visualization"
    ZEN = "zen"
    TRANSCENDENTAL = "transcendental"
    PRAYER = "prayer"


class MeditationLevel(Enum):
    """Meditation experience levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MeditationSystem:
    """Comprehensive meditation system with cultural adaptations"""
    
    def __init__(self):
        """Initialize meditation system"""
        self.meditation_sessions = {}
        self.user_progress = {}
        self.cultural_practices = self._load_cultural_practices()
        self.guided_sessions = self._load_guided_sessions()
        
        logger.info("Meditation system initialized")
    
    def _load_cultural_practices(self) -> Dict[str, Dict[str, Any]]:
        """Load meditation practices from different cultures"""
        return {
            'western': {
                'mindfulness': {
                    'name': 'Mindfulness Meditation',
                    'description': 'Focus on present moment awareness without judgment',
                    'instructions': [
                        "Find a comfortable seated position",
                        "Close your eyes gently or soften your gaze",
                        "Notice your breath without trying to change it",
                        "When thoughts arise, acknowledge them and return to breath",
                        "End with gratitude for taking this time"
                    ],
                    'duration_options': [5, 10, 15, 20, 30],
                    'benefits': ['stress reduction', 'improved focus', 'emotional regulation']
                },
                'body_scan': {
                    'name': 'Progressive Body Scan',
                    'description': 'Systematic awareness of physical sensations',
                    'instructions': [
                        "Lie down comfortably or sit with good posture",
                        "Start by noticing your breath",
                        "Slowly move attention from toes to head",
                        "Notice sensations without trying to change them",
                        "End by feeling your body as a whole"
                    ],
                    'duration_options': [10, 15, 20, 30, 45],
                    'benefits': ['body awareness', 'relaxation', 'tension release']
                }
            },
            'eastern': {
                'zen': {
                    'name': 'Zen Meditation (Zazen)',
                    'description': 'Sitting meditation focused on just being',
                    'instructions': [
                        "Sit in lotus or comfortable cross-legged position",
                        "Keep spine straight, hands in mudra position",
                        "Breathe naturally through nose",
                        "Let thoughts come and go like clouds",
                        "Simply sit and be present"
                    ],
                    'duration_options': [10, 20, 30, 45, 60],
                    'benefits': ['inner peace', 'wisdom', 'enlightenment']
                },
                'vipassana': {
                    'name': 'Vipassana (Insight Meditation)',
                    'description': 'Developing clear awareness of reality',
                    'instructions': [
                        "Sit comfortably with eyes closed",
                        "Observe breath at nostrils",
                        "Notice arising and passing of sensations",
                        "Maintain equanimity with all experiences",
                        "Cultivate wisdom through observation"
                    ],
                    'duration_options': [15, 30, 45, 60, 90],
                    'benefits': ['insight', 'liberation', 'equanimity']
                },
                'loving_kindness': {
                    'name': 'Metta (Loving-Kindness)',
                    'description': 'Cultivating universal love and compassion',
                    'instructions': [
                        "Begin with self-love: 'May I be happy and peaceful'",
                        "Extend to loved ones: 'May you be happy and peaceful'",
                        "Include neutral people in your awareness",
                        "Send love to difficult people",
                        "Embrace all beings with loving-kindness"
                    ],
                    'duration_options': [10, 15, 20, 30, 45],
                    'benefits': ['compassion', 'emotional healing', 'connection']
                }
            },
            'african': {
                'ancestral_connection': {
                    'name': 'Ancestral Wisdom Meditation',
                    'description': 'Connecting with ancestral guidance and strength',
                    'instructions': [
                        "Sit facing east (direction of new beginnings)",
                        "Call upon your ancestors for guidance",
                        "Feel their presence and wisdom within you",
                        "Listen for messages from the spirit world",
                        "Thank your ancestors before closing"
                    ],
                    'duration_options': [15, 20, 30, 45],
                    'benefits': ['wisdom', 'strength', 'spiritual connection']
                },
                'earth_grounding': {
                    'name': 'Earth Grounding Meditation',
                    'description': 'Connecting with Mother Earth\'s energy',
                    'instructions': [
                        "Sit or stand barefoot on natural ground",
                        "Feel your connection to the earth",
                        "Visualize roots growing from your feet",
                        "Draw strength from the earth\'s energy",
                        "Send gratitude to Mother Earth"
                    ],
                    'duration_options': [10, 15, 20, 30],
                    'benefits': ['grounding', 'stability', 'natural connection']
                }
            },
            'latin': {
                'corazon_meditation': {
                    'name': 'Meditación del Corazón (Heart Meditation)',
                    'description': 'Opening the heart to love and healing',
                    'instructions': [
                        "Place hand over heart, feel it beating",
                        "Breathe love into your heart center",
                        "Think of family and loved ones",
                        "Send amor to those who need healing",
                        "Let your heart overflow with compassion"
                    ],
                    'duration_options': [10, 15, 20, 30],
                    'benefits': ['heart opening', 'family connection', 'emotional healing']
                },
                'gratitude_prayer': {
                    'name': 'Gratitude Prayer Meditation',
                    'description': 'Combining prayer with meditative gratitude',
                    'instructions': [
                        "Begin with a prayer of gratitude",
                        "Reflect on blessings in your life",
                        "Thank the divine for guidance",
                        "Pray for family and community",
                        "End with faith and hope"
                    ],
                    'duration_options': [10, 15, 20, 30],
                    'benefits': ['gratitude', 'faith', 'spiritual connection']
                }
            },
            'indigenous': {
                'four_directions': {
                    'name': 'Four Directions Meditation',
                    'description': 'Honoring the wisdom of the four directions',
                    'instructions': [
                        "Face each direction (East, South, West, North)",
                        "Honor the teachings of each direction",
                        "East: new beginnings, South: growth",
                        "West: introspection, North: wisdom",
                        "Return to center, feeling balanced"
                    ],
                    'duration_options': [15, 20, 30, 45],
                    'benefits': ['balance', 'wisdom', 'spiritual guidance']
                },
                'nature_connection': {
                    'name': 'Nature Spirit Meditation',
                    'description': 'Connecting with the spirits of nature',
                    'instructions': [
                        "Find a peaceful place in nature",
                        "Acknowledge the spirits of the land",
                        "Listen to the voices of nature",
                        "Feel your interconnection with all life",
                        "Offer tobacco or prayers in gratitude"
                    ],
                    'duration_options': [15, 20, 30, 45],
                    'benefits': ['nature connection', 'spiritual awareness', 'harmony']
                }
            }
        }
    
    def _load_guided_sessions(self) -> Dict[str, List[str]]:
        """Load guided meditation scripts"""
        return {
            'breathing_5min': [
                "Welcome to this 5-minute breathing meditation.",
                "Find a comfortable position and close your eyes.",
                "Take three deep breaths to settle in.",
                "Now breathe naturally, focusing on each inhale and exhale.",
                "When your mind wanders, gently return to your breath.",
                "Continue breathing mindfully for the next few minutes.",
                "As we finish, take one more deep breath.",
                "Slowly open your eyes when you're ready."
            ],
            'body_scan_10min': [
                "Welcome to this 10-minute body scan meditation.",
                "Lie down comfortably and close your eyes.",
                "Begin by noticing your breath.",
                "Now bring attention to your toes.",
                "Notice any sensations without judgment.",
                "Slowly move up to your feet, ankles, and calves.",
                "Continue scanning each part of your body.",
                "Notice your chest rising and falling with breath.",
                "Scan your arms, hands, neck, and head.",
                "Feel your body as a complete whole.",
                "Take a moment to appreciate this awareness.",
                "When ready, slowly wiggle fingers and toes.",
                "Open your eyes and return to your day."
            ],
            'loving_kindness_15min': [
                "Welcome to loving-kindness meditation.",
                "Sit comfortably and close your eyes.",
                "Begin by sending love to yourself.",
                "'May I be happy, may I be peaceful, may I be free from suffering.'",
                "Feel this love filling your heart.",
                "Now think of someone you love deeply.",
                "'May you be happy, may you be peaceful, may you be free from suffering.'",
                "Visualize them surrounded by love and light.",
                "Now think of someone neutral to you.",
                "Send them the same loving wishes.",
                "Think of someone you find difficult.",
                "Even to them, send wishes of peace and happiness.",
                "Finally, extend love to all beings everywhere.",
                "'May all beings be happy and free.'",
                "Rest in this universal love for a moment.",
                "When ready, gently open your eyes."
            ]
        }
    
    async def start_meditation_session(
        self, 
        user_id: str, 
        meditation_type: str,
        duration: int,
        cultural_context: Dict[str, Any],
        level: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Start a new meditation session
        
        Args:
            user_id: User identifier
            meditation_type: Type of meditation
            duration: Duration in minutes
            cultural_context: Cultural adaptation context
            level: User's experience level
            
        Returns:
            Dict containing session information
        """
        try:
            session_id = f"session_{user_id}_{datetime.now().timestamp()}"
            cultural_region = cultural_context.get('cultural_region', 'western')
            
            # Get appropriate meditation practice
            practice = self._get_meditation_practice(meditation_type, cultural_region)
            
            if not practice:
                # Fallback to western mindfulness
                practice = self.cultural_practices['western']['mindfulness']
            
            # Create session
            session = {
                'session_id': session_id,
                'user_id': user_id,
                'meditation_type': meditation_type,
                'cultural_region': cultural_region,
                'duration': duration,
                'level': level,
                'practice': practice,
                'started_at': datetime.now().isoformat(),
                'status': 'active',
                'progress': 0,
                'guidance': self._get_session_guidance(meditation_type, duration, cultural_region)
            }
            
            # Store session
            self.meditation_sessions[session_id] = session
            
            # Update user progress
            await self._update_user_progress(user_id, meditation_type, duration)
            
            logger.info(f"Started meditation session {session_id} for user {user_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to start meditation session: {e}")
            raise ModelError(f"Meditation session start failed: {e}", "MODEL_002")
    
    def _get_meditation_practice(self, meditation_type: str, cultural_region: str) -> Optional[Dict[str, Any]]:
        """Get meditation practice based on type and culture"""
        cultural_practices = self.cultural_practices.get(cultural_region, {})
        
        # Direct match
        if meditation_type in cultural_practices:
            return cultural_practices[meditation_type]
        
        # Fuzzy matching for common types
        type_mapping = {
            'mindfulness': ['mindfulness', 'vipassana'],
            'breathing': ['breathing', 'mindfulness'],
            'body_scan': ['body_scan'],
            'loving_kindness': ['loving_kindness', 'metta', 'corazon_meditation'],
            'zen': ['zen', 'zazen'],
            'walking': ['walking', 'nature_connection'],
            'prayer': ['gratitude_prayer', 'prayer']
        }
        
        for mapped_type in type_mapping.get(meditation_type, []):
            if mapped_type in cultural_practices:
                return cultural_practices[mapped_type]
        
        return None
    
    def _get_session_guidance(self, meditation_type: str, duration: int, cultural_region: str) -> List[str]:
        """Get guided meditation instructions"""
        # Use pre-written guides for common combinations
        guide_key = f"{meditation_type}_{duration}min"
        if guide_key in self.guided_sessions:
            return self.guided_sessions[guide_key]
        
        # Generate dynamic guidance
        practice = self._get_meditation_practice(meditation_type, cultural_region)
        if practice:
            instructions = practice.get('instructions', [])
            
            # Add timing guidance
            guidance = [
                f"Welcome to this {duration}-minute {practice['name']} session.",
                "Find a comfortable position and settle in."
            ]
            
            guidance.extend(instructions[:3])  # First few instructions
            
            guidance.extend([
                f"Continue this practice for the next {duration-2} minutes.",
                "Stay present and gentle with yourself.",
                "As we finish, take a moment to appreciate your practice.",
                "When ready, slowly return to your day."
            ])
            
            return guidance
        
        # Default guidance
        return [
            f"Welcome to this {duration}-minute meditation session.",
            "Close your eyes and focus on your breath.",
            "Let thoughts come and go naturally.",
            "When ready, gently open your eyes."
        ]
    
    async def _update_user_progress(self, user_id: str, meditation_type: str, duration: int):
        """Update user's meditation progress"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {
                'total_sessions': 0,
                'total_minutes': 0,
                'types_practiced': {},
                'streak_days': 0,
                'last_session': None,
                'achievements': []
            }
        
        progress = self.user_progress[user_id]
        
        # Update counters
        progress['total_sessions'] += 1
        progress['total_minutes'] += duration
        
        # Update type practice
        if meditation_type not in progress['types_practiced']:
            progress['types_practiced'][meditation_type] = 0
        progress['types_practiced'][meditation_type] += 1
        
        # Update streak
        today = datetime.now().date()
        last_session_date = None
        
        if progress['last_session']:
            last_session_date = datetime.fromisoformat(progress['last_session']).date()
        
        if last_session_date == today:
            # Same day, no streak change
            pass
        elif last_session_date == today - timedelta(days=1):
            # Consecutive day
            progress['streak_days'] += 1
        elif not last_session_date or last_session_date < today - timedelta(days=1):
            # Gap or first session
            progress['streak_days'] = 1
        
        progress['last_session'] = datetime.now().isoformat()
        
        # Check for achievements
        await self._check_achievements(user_id, progress)
    
    async def _check_achievements(self, user_id: str, progress: Dict[str, Any]):
        """Check and award meditation achievements"""
        achievements = progress.get('achievements', [])
        new_achievements = []
        
        # Session milestones
        session_milestones = {
            1: "First Meditation",
            10: "Dedicated Practitioner", 
            50: "Meditation Enthusiast",
            100: "Zen Master",
            365: "Enlightened One"
        }
        
        for milestone, name in session_milestones.items():
            if progress['total_sessions'] >= milestone and name not in achievements:
                new_achievements.append(name)
                achievements.append(name)
        
        # Time milestones (in minutes)
        time_milestones = {
            60: "One Hour Club",
            300: "Five Hour Warrior",
            1000: "Meditation Master",
            5000: "Time Transcender"
        }
        
        for milestone, name in time_milestones.items():
            if progress['total_minutes'] >= milestone and name not in achievements:
                new_achievements.append(name)
                achievements.append(name)
        
        # Streak achievements
        streak_milestones = {
            7: "Week Warrior",
            30: "Monthly Master",
            100: "Consistency Champion",
            365: "Year-long Yogi"
        }
        
        for milestone, name in streak_milestones.items():
            if progress['streak_days'] >= milestone and name not in achievements:
                new_achievements.append(name)
                achievements.append(name)
        
        # Variety achievements
        if len(progress['types_practiced']) >= 3 and "Variety Explorer" not in achievements:
            new_achievements.append("Variety Explorer")
            achievements.append("Variety Explorer")
        
        if new_achievements:
            logger.info(f"User {user_id} earned achievements: {new_achievements}")
    
    async def complete_meditation_session(
        self, 
        session_id: str, 
        completed_duration: int,
        rating: Optional[int] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete a meditation session
        
        Args:
            session_id: Session identifier
            completed_duration: Actual duration completed
            rating: Session rating (1-5)
            notes: Optional session notes
            
        Returns:
            Dict containing completion information
        """
        try:
            if session_id not in self.meditation_sessions:
                raise ValueError("Session not found")
            
            session = self.meditation_sessions[session_id]
            
            # Update session
            session.update({
                'completed_at': datetime.now().isoformat(),
                'completed_duration': completed_duration,
                'rating': rating,
                'notes': notes,
                'status': 'completed'
            })
            
            # Calculate completion percentage
            planned_duration = session['duration']
            completion_percentage = min(100, (completed_duration / planned_duration) * 100)
            session['completion_percentage'] = completion_percentage
            
            # Generate session insights
            insights = self._generate_session_insights(session)
            session['insights'] = insights
            
            logger.info(f"Completed meditation session {session_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to complete meditation session: {e}")
            raise ModelError(f"Session completion failed: {e}", "MODEL_002")
    
    def _generate_session_insights(self, session: Dict[str, Any]) -> List[str]:
        """Generate insights from completed session"""
        insights = []
        
        completion = session.get('completion_percentage', 0)
        rating = session.get('rating')
        duration = session.get('completed_duration', 0)
        
        # Completion insights
        if completion >= 100:
            insights.append("Congratulations on completing your full meditation session!")
        elif completion >= 75:
            insights.append("Great job! You completed most of your meditation session.")
        elif completion >= 50:
            insights.append("Good effort! Even partial meditation has benefits.")
        else:
            insights.append("Every moment of meditation counts. Keep practicing!")
        
        # Rating insights
        if rating:
            if rating >= 4:
                insights.append("You're finding great value in your meditation practice!")
            elif rating >= 3:
                insights.append("Your meditation practice is developing well.")
            else:
                insights.append("Consider trying different meditation types to find what works best.")
        
        # Duration insights
        if duration >= 20:
            insights.append("Longer meditation sessions deepen your practice significantly.")
        elif duration >= 10:
            insights.append("This is a perfect duration for building consistency.")
        else:
            insights.append("Short sessions are a great way to start your meditation journey.")
        
        return insights[:2]  # Limit to 2 insights
    
    async def get_meditation_recommendations(
        self, 
        user_id: str, 
        cultural_context: Dict[str, Any],
        current_mood: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get personalized meditation recommendations
        
        Args:
            user_id: User identifier
            cultural_context: Cultural context
            current_mood: Current mood level (1-5)
            
        Returns:
            List of recommended meditations
        """
        try:
            cultural_region = cultural_context.get('cultural_region', 'western')
            user_progress = self.user_progress.get(user_id, {})
            
            recommendations = []
            
            # Get cultural practices
            cultural_practices = self.cultural_practices.get(cultural_region, self.cultural_practices['western'])
            
            # Mood-based recommendations
            if current_mood:
                if current_mood <= 2:  # Low mood
                    # Recommend uplifting practices
                    if cultural_region == 'eastern':
                        recommendations.append({
                            'type': 'loving_kindness',
                            'duration': 15,
                            'reason': 'Loving-kindness meditation can help lift your spirits'
                        })
                    elif cultural_region == 'african':
                        recommendations.append({
                            'type': 'ancestral_connection',
                            'duration': 20,
                            'reason': 'Connect with ancestral strength for support'
                        })
                    else:
                        recommendations.append({
                            'type': 'body_scan',
                            'duration': 10,
                            'reason': 'Body scan can help release tension and stress'
                        })
                
                elif current_mood >= 4:  # Good mood
                    recommendations.append({
                        'type': 'gratitude_prayer' if cultural_region == 'latin' else 'mindfulness',
                        'duration': 10,
                        'reason': 'Cultivate and appreciate this positive state'
                    })
            
            # Experience-based recommendations
            total_sessions = user_progress.get('total_sessions', 0)
            
            if total_sessions == 0:  # Beginner
                recommendations.append({
                    'type': 'breathing',
                    'duration': 5,
                    'reason': 'Perfect introduction to meditation'
                })
            elif total_sessions < 10:  # Early practitioner
                recommendations.append({
                    'type': 'mindfulness',
                    'duration': 10,
                    'reason': 'Build your foundation with mindfulness'
                })
            else:  # Experienced
                # Recommend variety
                practiced_types = set(user_progress.get('types_practiced', {}).keys())
                available_types = set(cultural_practices.keys())
                new_types = available_types - practiced_types
                
                if new_types:
                    new_type = random.choice(list(new_types))
                    recommendations.append({
                        'type': new_type,
                        'duration': 15,
                        'reason': 'Explore a new meditation style'
                    })
            
            # Daily practice recommendation
            recommendations.append({
                'type': 'mindfulness',
                'duration': 10,
                'reason': 'Great for daily practice and consistency'
            })
            
            return recommendations[:3]  # Limit to 3 recommendations
            
        except Exception as e:
            logger.error(f"Failed to get meditation recommendations: {e}")
            return []
    
    async def get_user_meditation_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user's meditation statistics"""
        try:
            if user_id not in self.user_progress:
                return {'error': 'No meditation data found for user'}
            
            progress = self.user_progress[user_id]
            
            # Calculate additional stats
            stats = progress.copy()
            
            # Average session length
            if stats['total_sessions'] > 0:
                stats['average_session_length'] = stats['total_minutes'] / stats['total_sessions']
            else:
                stats['average_session_length'] = 0
            
            # Most practiced type
            if stats['types_practiced']:
                most_practiced = max(stats['types_practiced'].items(), key=lambda x: x[1])
                stats['favorite_practice'] = most_practiced[0]
                stats['favorite_practice_count'] = most_practiced[1]
            
            # Recent activity
            if stats['last_session']:
                last_session_date = datetime.fromisoformat(stats['last_session']).date()
                days_since_last = (datetime.now().date() - last_session_date).days
                stats['days_since_last_session'] = days_since_last
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get meditation stats: {e}")
            raise ModelError(f"Meditation stats retrieval failed: {e}", "MODEL_002")
    
    async def get_available_practices(self, cultural_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available meditation practices for user's culture"""
        cultural_region = cultural_context.get('cultural_region', 'western')
        practices = self.cultural_practices.get(cultural_region, self.cultural_practices['western'])
        
        return [
            {
                'type': practice_type,
                'name': practice_data['name'],
                'description': practice_data['description'],
                'duration_options': practice_data['duration_options'],
                'benefits': practice_data['benefits']
            }
            for practice_type, practice_data in practices.items()
        ]

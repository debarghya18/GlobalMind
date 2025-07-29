"""
Mood tracking system for GlobalMind
Provides culturally-adaptive mood monitoring and analytics
"""

import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
import json
from enum import Enum

from ..core.exceptions import ModelError


class MoodLevel(Enum):
    """Mood level enumeration"""
    VERY_LOW = 1
    LOW = 2
    NEUTRAL = 3
    GOOD = 4
    VERY_GOOD = 5


class MoodTracker:
    """Advanced mood tracking with cultural adaptations"""
    
    def __init__(self):
        """Initialize mood tracker"""
        self.mood_history = {}
        self.cultural_mood_expressions = self._load_cultural_expressions()
        self.mood_factors = self._load_mood_factors()
        
        logger.info("Mood tracker initialized")
    
    def _load_cultural_expressions(self) -> Dict[str, Dict[str, List[str]]]:
        """Load culturally-specific mood expressions"""
        return {
            'western': {
                'very_good': ['fantastic', 'amazing', 'excellent', 'wonderful', 'great'],
                'good': ['happy', 'content', 'pleased', 'satisfied', 'positive'],
                'neutral': ['okay', 'fine', 'alright', 'so-so', 'average'],
                'low': ['sad', 'down', 'blue', 'disappointed', 'unhappy'],
                'very_low': ['terrible', 'awful', 'depressed', 'miserable', 'devastating']
            },
            'eastern': {
                'very_good': ['blessed', 'harmonious', 'peaceful', 'balanced', 'enlightened'],
                'good': ['content', 'serene', 'calm', 'grateful', 'centered'],
                'neutral': ['balanced', 'steady', 'stable', 'moderate', 'even'],
                'low': ['unbalanced', 'disturbed', 'unsettled', 'restless', 'heavy'],
                'very_low': ['suffering', 'tormented', 'lost', 'broken', 'overwhelmed']
            },
            'african': {
                'very_good': ['blessed', 'strong', 'powerful', 'connected', 'whole'],
                'good': ['good spirit', 'uplifted', 'supported', 'community-strong', 'proud'],
                'neutral': ['steady', 'walking forward', 'managing', 'surviving', 'holding on'],
                'low': ['heavy heart', 'disconnected', 'struggling', 'weary', 'burdened'],
                'very_low': ['broken spirit', 'lost way', 'deep pain', 'abandoned', 'suffering']
            },
            'latin': {
                'very_good': ['fantástico', 'bendecido', 'alegre', 'fuerte', 'orgulloso'],
                'good': ['bien', 'feliz', 'contento', 'animado', 'positivo'],
                'neutral': ['regular', 'normal', 'así así', 'tranquilo', 'estable'],
                'low': ['triste', 'preocupado', 'desanimado', 'cansado', 'melancólico'],
                'very_low': ['muy mal', 'desesperado', 'perdido', 'sin esperanza', 'sufriendo']
            }
        }
    
    def _load_mood_factors(self) -> Dict[str, List[str]]:
        """Load factors that influence mood"""
        return {
            'physical': ['sleep', 'exercise', 'nutrition', 'illness', 'energy', 'pain'],
            'emotional': ['stress', 'anxiety', 'relationships', 'love', 'anger', 'fear'],
            'social': ['family', 'friends', 'work', 'community', 'isolation', 'support'],
            'spiritual': ['meaning', 'purpose', 'meditation', 'prayer', 'nature', 'gratitude'],
            'environmental': ['weather', 'location', 'home', 'safety', 'comfort', 'space'],
            'cognitive': ['thoughts', 'focus', 'creativity', 'learning', 'memory', 'clarity']
        }
    
    async def record_mood(
        self, 
        user_id: str, 
        mood_level: int, 
        cultural_context: Dict[str, Any],
        factors: List[str] = None,
        notes: str = None
    ) -> Dict[str, Any]:
        """
        Record user mood with cultural context
        
        Args:
            user_id: User identifier
            mood_level: Mood level (1-5)
            cultural_context: Cultural adaptation context
            factors: Contributing factors
            notes: Optional notes
            
        Returns:
            Dict containing mood record
        """
        try:
            timestamp = datetime.now()
            
            # Validate mood level
            if not 1 <= mood_level <= 5:
                raise ValueError("Mood level must be between 1 and 5")
            
            # Create mood record
            mood_record = {
                'user_id': user_id,
                'timestamp': timestamp.isoformat(),
                'mood_level': mood_level,
                'mood_name': self._get_mood_name(mood_level),
                'cultural_context': cultural_context,
                'factors': factors or [],
                'notes': notes,
                'cultural_expression': self._get_cultural_expression(mood_level, cultural_context),
                'recommendations': await self._generate_recommendations(mood_level, cultural_context, factors)
            }
            
            # Store in history
            if user_id not in self.mood_history:
                self.mood_history[user_id] = []
            
            self.mood_history[user_id].append(mood_record)
            
            # Keep only last 365 days
            cutoff_date = timestamp - timedelta(days=365)
            self.mood_history[user_id] = [
                record for record in self.mood_history[user_id]
                if datetime.fromisoformat(record['timestamp']) > cutoff_date
            ]
            
            logger.info(f"Recorded mood {mood_level} for user {user_id}")
            return mood_record
            
        except Exception as e:
            logger.error(f"Failed to record mood: {e}")
            raise ModelError(f"Mood recording failed: {e}", "MODEL_002")
    
    def _get_mood_name(self, mood_level: int) -> str:
        """Get mood name from level"""
        mood_names = {
            1: 'Very Low',
            2: 'Low', 
            3: 'Neutral',
            4: 'Good',
            5: 'Very Good'
        }
        return mood_names.get(mood_level, 'Unknown')
    
    def _get_cultural_expression(self, mood_level: int, cultural_context: Dict[str, Any]) -> str:
        """Get culturally appropriate mood expression"""
        cultural_region = cultural_context.get('cultural_region', 'western')
        expressions = self.cultural_mood_expressions.get(cultural_region, self.cultural_mood_expressions['western'])
        
        mood_key_map = {
            1: 'very_low',
            2: 'low',
            3: 'neutral', 
            4: 'good',
            5: 'very_good'
        }
        
        mood_key = mood_key_map.get(mood_level, 'neutral')
        expression_list = expressions.get(mood_key, ['feeling okay'])
        
        return expression_list[0] if expression_list else 'feeling okay'
    
    async def _generate_recommendations(
        self, 
        mood_level: int, 
        cultural_context: Dict[str, Any], 
        factors: List[str]
    ) -> List[str]:
        """Generate culturally-appropriate mood recommendations"""
        cultural_region = cultural_context.get('cultural_region', 'western')
        
        recommendations = []
        
        if mood_level <= 2:  # Low mood
            if cultural_region == 'western':
                recommendations.extend([
                    "Consider reaching out to a friend or family member",
                    "Try some gentle physical activity like a walk",
                    "Practice deep breathing or mindfulness",
                    "Engage in a hobby you enjoy"
                ])
            elif cultural_region == 'eastern':
                recommendations.extend([
                    "Practice meditation or mindful breathing",
                    "Spend time in nature to restore balance",
                    "Consider tai chi or gentle movement",
                    "Reflect on what brings harmony to your life"
                ])
            elif cultural_region == 'african':
                recommendations.extend([
                    "Connect with your community or family",
                    "Listen to uplifting music or traditional songs",
                    "Spend time outdoors and connect with nature",
                    "Remember your strength and resilience"
                ])
            elif cultural_region == 'latin':
                recommendations.extend([
                    "Connect with familia and friends",
                    "Listen to music that lifts your spirit",
                    "Consider prayer or spiritual reflection",
                    "Engage in creative expression"
                ])
        
        elif mood_level >= 4:  # Good mood
            recommendations.extend([
                "Celebrate this positive moment",
                "Share your joy with others",
                "Use this energy for meaningful activities",
                "Practice gratitude for what's going well"
            ])
        
        else:  # Neutral mood
            recommendations.extend([
                "Consider activities that usually bring you joy",
                "Check in with your physical needs (rest, nutrition)",
                "Connect with supportive people in your life",
                "Set a small, achievable goal for today"
            ])
        
        # Add factor-specific recommendations
        if factors:
            if 'sleep' in factors:
                recommendations.append("Focus on improving sleep quality tonight")
            if 'exercise' in factors:
                recommendations.append("Consider gentle movement or exercise")
            if 'relationships' in factors:
                recommendations.append("Reach out to supportive people in your life")
            if 'stress' in factors:
                recommendations.append("Try stress-reduction techniques like deep breathing")
        
        return recommendations[:4]  # Limit to 4 recommendations
    
    async def get_mood_trends(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get mood trends and analytics
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Dict containing trend analysis
        """
        try:
            if user_id not in self.mood_history:
                return {'error': 'No mood data found for user'}
            
            # Get recent records
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_records = [
                record for record in self.mood_history[user_id]
                if datetime.fromisoformat(record['timestamp']) > cutoff_date
            ]
            
            if not recent_records:
                return {'error': 'No recent mood data found'}
            
            # Calculate trends
            moods = [record['mood_level'] for record in recent_records]
            
            trends = {
                'total_entries': len(recent_records),
                'average_mood': sum(moods) / len(moods),
                'mood_distribution': {
                    'very_low': len([m for m in moods if m == 1]),
                    'low': len([m for m in moods if m == 2]),
                    'neutral': len([m for m in moods if m == 3]),
                    'good': len([m for m in moods if m == 4]),
                    'very_good': len([m for m in moods if m == 5])
                },
                'trend_direction': self._calculate_trend_direction(moods),
                'common_factors': self._get_common_factors(recent_records),
                'best_day': max(recent_records, key=lambda x: x['mood_level']),
                'challenging_day': min(recent_records, key=lambda x: x['mood_level']),
                'mood_stability': self._calculate_stability(moods),
                'insights': self._generate_insights(recent_records)
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Failed to get mood trends: {e}")
            raise ModelError(f"Mood trends analysis failed: {e}", "MODEL_002")
    
    def _calculate_trend_direction(self, moods: List[int]) -> str:
        """Calculate overall trend direction"""
        if len(moods) < 2:
            return 'insufficient_data'
        
        # Compare first half to second half
        mid_point = len(moods) // 2
        first_half_avg = sum(moods[:mid_point]) / mid_point
        second_half_avg = sum(moods[mid_point:]) / (len(moods) - mid_point)
        
        difference = second_half_avg - first_half_avg
        
        if difference > 0.5:
            return 'improving'
        elif difference < -0.5:
            return 'declining'
        else:
            return 'stable'
    
    def _get_common_factors(self, records: List[Dict[str, Any]]) -> List[str]:
        """Get most common mood factors"""
        factor_counts = {}
        
        for record in records:
            factors = record.get('factors', [])
            for factor in factors:
                factor_counts[factor] = factor_counts.get(factor, 0) + 1
        
        # Sort by frequency and return top 5
        sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)
        return [factor for factor, count in sorted_factors[:5]]
    
    def _calculate_stability(self, moods: List[int]) -> Dict[str, Any]:
        """Calculate mood stability metrics"""
        if len(moods) < 2:
            return {'stability_score': 1.0, 'description': 'insufficient_data'}
        
        # Calculate variance
        avg_mood = sum(moods) / len(moods)
        variance = sum((mood - avg_mood) ** 2 for mood in moods) / len(moods)
        
        # Convert to stability score (0-1, where 1 is most stable)
        stability_score = max(0, 1 - (variance / 4))  # Max variance is 4 (1 to 5 range)
        
        if stability_score >= 0.8:
            description = 'very_stable'
        elif stability_score >= 0.6:
            description = 'stable'
        elif stability_score >= 0.4:
            description = 'somewhat_variable'
        else:
            description = 'highly_variable'
        
        return {
            'stability_score': stability_score,
            'description': description,
            'variance': variance
        }
    
    def _generate_insights(self, records: List[Dict[str, Any]]) -> List[str]:
        """Generate insights from mood data"""
        insights = []
        
        if not records:
            return insights
        
        moods = [record['mood_level'] for record in records]
        avg_mood = sum(moods) / len(moods)
        
        # Average mood insight
        if avg_mood >= 4:
            insights.append("Your overall mood has been quite positive lately!")
        elif avg_mood <= 2:
            insights.append("You've been experiencing some challenging times. Consider reaching out for support.")
        else:
            insights.append("Your mood has been relatively balanced recently.")
        
        # Consistency insight
        stability = self._calculate_stability(moods)
        if stability['stability_score'] >= 0.8:
            insights.append("Your mood has been quite stable, which is a positive sign.")
        elif stability['stability_score'] <= 0.4:
            insights.append("Your mood has been variable. Consider tracking factors that might be influencing these changes.")
        
        # Factor insights
        common_factors = self._get_common_factors(records)
        if common_factors:
            top_factor = common_factors[0]
            insights.append(f"'{top_factor}' appears to be a significant factor in your mood patterns.")
        
        # Trend insight
        trend = self._calculate_trend_direction(moods)
        if trend == 'improving':
            insights.append("There's a positive trend in your recent mood entries!")
        elif trend == 'declining':
            insights.append("Your mood trend shows some decline. Consider additional self-care strategies.")
        
        return insights[:3]  # Limit to 3 key insights
    
    async def get_mood_suggestions(self, current_mood: int, cultural_context: Dict[str, Any]) -> List[str]:
        """Get immediate mood-based suggestions"""
        return await self._generate_recommendations(current_mood, cultural_context, [])
    
    async def export_mood_data(self, user_id: str) -> Dict[str, Any]:
        """Export user's mood data"""
        try:
            if user_id not in self.mood_history:
                return {'error': 'No mood data found'}
            
            return {
                'user_id': user_id,
                'export_date': datetime.now().isoformat(),
                'total_entries': len(self.mood_history[user_id]),
                'mood_records': self.mood_history[user_id]
            }
            
        except Exception as e:
            logger.error(f"Failed to export mood data: {e}")
            raise ModelError(f"Mood data export failed: {e}", "MODEL_002")
    
    async def delete_mood_data(self, user_id: str):
        """Delete user's mood data"""
        try:
            if user_id in self.mood_history:
                del self.mood_history[user_id]
                logger.info(f"Deleted mood data for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to delete mood data: {e}")
            raise ModelError(f"Mood data deletion failed: {e}", "MODEL_002")

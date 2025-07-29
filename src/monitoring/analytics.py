"""
Advanced Analytics module for GlobalMind
Provides comprehensive analytics and insights for mental health progress
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from loguru import logger
import json
from dataclasses import dataclass
from enum import Enum

from ..core.exceptions import AnalyticsError
from ..storage.database import DatabaseManager


class MoodLevel(Enum):
    """Mood level enumeration"""
    VERY_LOW = 1
    LOW = 2
    NEUTRAL = 3
    GOOD = 4
    VERY_GOOD = 5


class AnalyticsType(Enum):
    """Analytics type enumeration"""
    MOOD_TRACKING = "mood_tracking"
    PROGRESS_MONITORING = "progress_monitoring"
    USAGE_ANALYTICS = "usage_analytics"
    CRISIS_ANALYTICS = "crisis_analytics"
    CULTURAL_ANALYTICS = "cultural_analytics"


@dataclass
class MoodEntry:
    """Mood tracking entry"""
    timestamp: datetime
    mood_level: MoodLevel
    notes: Optional[str] = None
    triggers: Optional[List[str]] = None
    activities: Optional[List[str]] = None
    user_id: Optional[str] = None


@dataclass
class ProgressMetric:
    """Progress tracking metric"""
    metric_name: str
    value: float
    timestamp: datetime
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class UsageMetric:
    """Usage analytics metric"""
    session_id: str
    user_id: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    messages_exchanged: int
    languages_used: List[str]
    cultural_context: Optional[str]
    crisis_detected: bool = False


class AdvancedAnalytics:
    """Advanced analytics engine for GlobalMind"""
    
    def __init__(self, database_manager: DatabaseManager):
        """
        Initialize analytics engine
        
        Args:
            database_manager: Database manager instance
        """
        self.database_manager = database_manager
        self.analytics_cache = {}
        self.metrics_buffer = []
        
        logger.info("Advanced Analytics engine initialized")
    
    async def track_mood(self, mood_entry: MoodEntry) -> bool:
        """
        Track user mood entry
        
        Args:
            mood_entry: Mood entry to track
            
        Returns:
            bool: True if successful
        """
        try:
            # Store mood entry in database
            await self.database_manager.store_mood_entry(mood_entry)
            
            # Update real-time analytics
            await self._update_mood_analytics(mood_entry)
            
            logger.info(f"Mood tracked: {mood_entry.mood_level.name}")
            return True
            
        except Exception as e:
            logger.error(f"Mood tracking failed: {e}")
            raise AnalyticsError(f"Mood tracking failed: {e}", "ANALYTICS_001")
    
    async def track_progress(self, progress_metric: ProgressMetric) -> bool:
        """
        Track progress metric
        
        Args:
            progress_metric: Progress metric to track
            
        Returns:
            bool: True if successful
        """
        try:
            # Store progress metric in database
            await self.database_manager.store_progress_metric(progress_metric)
            
            # Update progress analytics
            await self._update_progress_analytics(progress_metric)
            
            logger.info(f"Progress tracked: {progress_metric.metric_name}")
            return True
            
        except Exception as e:
            logger.error(f"Progress tracking failed: {e}")
            raise AnalyticsError(f"Progress tracking failed: {e}", "ANALYTICS_002")
    
    async def track_usage(self, usage_metric: UsageMetric) -> bool:
        """
        Track usage metric
        
        Args:
            usage_metric: Usage metric to track
            
        Returns:
            bool: True if successful
        """
        try:
            # Store usage metric in database
            await self.database_manager.store_usage_metric(usage_metric)
            
            # Update usage analytics
            await self._update_usage_analytics(usage_metric)
            
            logger.info(f"Usage tracked: {usage_metric.session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Usage tracking failed: {e}")
            raise AnalyticsError(f"Usage tracking failed: {e}", "ANALYTICS_003")
    
    async def generate_mood_report(
        self, 
        user_id: Optional[str] = None, 
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate mood tracking report
        
        Args:
            user_id: User ID (if None, generate aggregate report)
            days: Number of days to include
            
        Returns:
            Dict[str, Any]: Mood report
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get mood entries from database
            mood_entries = await self.database_manager.get_mood_entries(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date
            )
            
            if not mood_entries:
                return {
                    'period': f"{days} days",
                    'total_entries': 0,
                    'message': 'No mood data available'
                }
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame([
                {
                    'timestamp': entry.timestamp,
                    'mood_level': entry.mood_level.value,
                    'notes': entry.notes,
                    'triggers': entry.triggers,
                    'activities': entry.activities
                }
                for entry in mood_entries
            ])
            
            # Calculate statistics
            mood_stats = {
                'total_entries': len(df),
                'average_mood': df['mood_level'].mean(),
                'mood_trend': self._calculate_mood_trend(df),
                'mood_distribution': df['mood_level'].value_counts().to_dict(),
                'best_day': df.loc[df['mood_level'].idxmax()]['timestamp'].isoformat(),
                'worst_day': df.loc[df['mood_level'].idxmin()]['timestamp'].isoformat(),
                'consistency_score': self._calculate_mood_consistency(df)
            }
            
            # Generate insights
            insights = self._generate_mood_insights(df)
            
            return {
                'period': f"{days} days",
                'statistics': mood_stats,
                'insights': insights,
                'recommendations': self._generate_mood_recommendations(df)
            }
            
        except Exception as e:
            logger.error(f"Mood report generation failed: {e}")
            raise AnalyticsError(f"Mood report generation failed: {e}", "ANALYTICS_004")
    
    async def generate_progress_report(
        self, 
        user_id: Optional[str] = None, 
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate progress tracking report
        
        Args:
            user_id: User ID (if None, generate aggregate report)
            days: Number of days to include
            
        Returns:
            Dict[str, Any]: Progress report
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get progress metrics from database
            progress_metrics = await self.database_manager.get_progress_metrics(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date
            )
            
            if not progress_metrics:
                return {
                    'period': f"{days} days",
                    'total_metrics': 0,
                    'message': 'No progress data available'
                }
            
            # Group by metric type
            metrics_by_type = {}
            for metric in progress_metrics:
                if metric.metric_name not in metrics_by_type:
                    metrics_by_type[metric.metric_name] = []
                metrics_by_type[metric.metric_name].append(metric)
            
            # Calculate progress for each metric
            progress_analysis = {}
            for metric_name, metrics in metrics_by_type.items():
                df = pd.DataFrame([
                    {
                        'timestamp': metric.timestamp,
                        'value': metric.value
                    }
                    for metric in metrics
                ])
                
                progress_analysis[metric_name] = {
                    'total_entries': len(df),
                    'current_value': df['value'].iloc[-1] if not df.empty else 0,
                    'initial_value': df['value'].iloc[0] if not df.empty else 0,
                    'improvement': self._calculate_improvement(df),
                    'trend': self._calculate_progress_trend(df),
                    'consistency': self._calculate_progress_consistency(df)
                }
            
            return {
                'period': f"{days} days",
                'metrics_analysis': progress_analysis,
                'overall_progress': self._calculate_overall_progress(progress_analysis),
                'recommendations': self._generate_progress_recommendations(progress_analysis)
            }
            
        except Exception as e:
            logger.error(f"Progress report generation failed: {e}")
            raise AnalyticsError(f"Progress report generation failed: {e}", "ANALYTICS_005")
    
    async def generate_usage_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate usage analytics report
        
        Args:
            days: Number of days to include
            
        Returns:
            Dict[str, Any]: Usage report
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get usage metrics from database
            usage_metrics = await self.database_manager.get_usage_metrics(
                start_date=start_date,
                end_date=end_date
            )
            
            if not usage_metrics:
                return {
                    'period': f"{days} days",
                    'total_sessions': 0,
                    'message': 'No usage data available'
                }
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame([
                {
                    'session_id': metric.session_id,
                    'user_id': metric.user_id,
                    'start_time': metric.start_time,
                    'end_time': metric.end_time,
                    'messages_exchanged': metric.messages_exchanged,
                    'languages_used': metric.languages_used,
                    'cultural_context': metric.cultural_context,
                    'crisis_detected': metric.crisis_detected
                }
                for metric in usage_metrics
            ])
            
            # Calculate usage statistics
            usage_stats = {
                'total_sessions': len(df),
                'unique_users': df['user_id'].nunique(),
                'average_messages_per_session': df['messages_exchanged'].mean(),
                'total_messages': df['messages_exchanged'].sum(),
                'language_distribution': self._calculate_language_distribution(df),
                'cultural_distribution': self._calculate_cultural_distribution(df),
                'crisis_detection_rate': df['crisis_detected'].mean(),
                'peak_usage_hours': self._calculate_peak_usage_hours(df)
            }
            
            return {
                'period': f"{days} days",
                'statistics': usage_stats,
                'insights': self._generate_usage_insights(df),
                'recommendations': self._generate_usage_recommendations(df)
            }
            
        except Exception as e:
            logger.error(f"Usage report generation failed: {e}")
            raise AnalyticsError(f"Usage report generation failed: {e}", "ANALYTICS_006")
    
    async def generate_crisis_analytics(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate crisis detection analytics
        
        Args:
            days: Number of days to include
            
        Returns:
            Dict[str, Any]: Crisis analytics
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get crisis events from database
            crisis_events = await self.database_manager.get_crisis_events(
                start_date=start_date,
                end_date=end_date
            )
            
            if not crisis_events:
                return {
                    'period': f"{days} days",
                    'total_events': 0,
                    'message': 'No crisis events detected'
                }
            
            # Analyze crisis patterns
            crisis_stats = {
                'total_events': len(crisis_events),
                'events_by_severity': self._analyze_crisis_severity(crisis_events),
                'temporal_patterns': self._analyze_crisis_timing(crisis_events),
                'cultural_patterns': self._analyze_crisis_cultural_context(crisis_events),
                'intervention_effectiveness': self._analyze_intervention_effectiveness(crisis_events)
            }
            
            return {
                'period': f"{days} days",
                'statistics': crisis_stats,
                'insights': self._generate_crisis_insights(crisis_events),
                'recommendations': self._generate_crisis_recommendations(crisis_events)
            }
            
        except Exception as e:
            logger.error(f"Crisis analytics generation failed: {e}")
            raise AnalyticsError(f"Crisis analytics generation failed: {e}", "ANALYTICS_007")
    
    def _calculate_mood_trend(self, df: pd.DataFrame) -> str:
        """Calculate mood trend from DataFrame"""
        if len(df) < 2:
            return "insufficient_data"
        
        # Calculate linear trend
        x = range(len(df))
        y = df['mood_level'].values
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_mood_consistency(self, df: pd.DataFrame) -> float:
        """Calculate mood consistency score"""
        if len(df) < 2:
            return 0.0
        
        # Calculate coefficient of variation
        cv = df['mood_level'].std() / df['mood_level'].mean()
        # Convert to consistency score (0-1, higher is more consistent)
        return max(0, 1 - cv)
    
    def _generate_mood_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate mood insights from DataFrame"""
        insights = []
        
        # Check for patterns
        if df['mood_level'].mean() > 3.5:
            insights.append("Your overall mood has been positive recently")
        elif df['mood_level'].mean() < 2.5:
            insights.append("Your mood has been low recently - consider reaching out for support")
        
        # Check for volatility
        if df['mood_level'].std() > 1.5:
            insights.append("Your mood has been quite variable - tracking triggers might help")
        
        # Check for trends
        trend = self._calculate_mood_trend(df)
        if trend == "improving":
            insights.append("Your mood trend is improving - keep up the good work!")
        elif trend == "declining":
            insights.append("Your mood trend is declining - consider additional support")
        
        return insights
    
    def _generate_mood_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate mood recommendations"""
        recommendations = []
        
        avg_mood = df['mood_level'].mean()
        
        if avg_mood < 2.5:
            recommendations.append("Consider scheduling regular check-ins with a mental health professional")
            recommendations.append("Try incorporating daily mindfulness or meditation practices")
        elif avg_mood < 3.5:
            recommendations.append("Focus on maintaining healthy sleep and exercise routines")
            recommendations.append("Consider journaling to identify mood patterns")
        else:
            recommendations.append("Continue your current practices - they're working well!")
            recommendations.append("Consider sharing your strategies with others who might benefit")
        
        return recommendations
    
    def _calculate_improvement(self, df: pd.DataFrame) -> float:
        """Calculate improvement percentage"""
        if len(df) < 2:
            return 0.0
        
        initial = df['value'].iloc[0]
        current = df['value'].iloc[-1]
        
        if initial == 0:
            return 0.0
        
        return ((current - initial) / initial) * 100
    
    def _calculate_progress_trend(self, df: pd.DataFrame) -> str:
        """Calculate progress trend"""
        if len(df) < 2:
            return "insufficient_data"
        
        # Calculate linear trend
        x = range(len(df))
        y = df['value'].values
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.01:
            return "improving"
        elif slope < -0.01:
            return "declining"
        else:
            return "stable"
    
    def _calculate_progress_consistency(self, df: pd.DataFrame) -> float:
        """Calculate progress consistency score"""
        if len(df) < 2:
            return 0.0
        
        # Calculate R-squared of linear fit
        x = range(len(df))
        y = df['value'].values
        
        # Fit linear regression
        coeffs = np.polyfit(x, y, 1)
        predicted = np.polyval(coeffs, x)
        
        # Calculate R-squared
        ss_res = np.sum((y - predicted) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        return 1 - (ss_res / ss_tot)
    
    def _calculate_overall_progress(self, progress_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall progress score"""
        if not progress_analysis:
            return {'score': 0, 'status': 'no_data'}
        
        # Calculate weighted average of improvements
        total_improvement = 0
        total_weight = 0
        
        for metric_name, analysis in progress_analysis.items():
            improvement = analysis.get('improvement', 0)
            weight = analysis.get('total_entries', 1)
            
            total_improvement += improvement * weight
            total_weight += weight
        
        if total_weight == 0:
            return {'score': 0, 'status': 'no_data'}
        
        avg_improvement = total_improvement / total_weight
        
        if avg_improvement > 10:
            status = 'excellent'
        elif avg_improvement > 5:
            status = 'good'
        elif avg_improvement > 0:
            status = 'improving'
        elif avg_improvement > -5:
            status = 'stable'
        else:
            status = 'declining'
        
        return {
            'score': avg_improvement,
            'status': status,
            'metrics_count': len(progress_analysis)
        }
    
    def _generate_progress_recommendations(self, progress_analysis: Dict[str, Any]) -> List[str]:
        """Generate progress recommendations"""
        recommendations = []
        
        overall_progress = self._calculate_overall_progress(progress_analysis)
        status = overall_progress.get('status', 'no_data')
        
        if status == 'excellent':
            recommendations.append("Outstanding progress! Continue your current approach")
        elif status == 'good':
            recommendations.append("Good progress! Consider setting new goals to maintain momentum")
        elif status == 'improving':
            recommendations.append("You're making progress! Stay consistent with your efforts")
        elif status == 'stable':
            recommendations.append("Consider adjusting your approach to see more improvement")
        else:
            recommendations.append("Progress has slowed - consider seeking additional support")
        
        return recommendations
    
    def _calculate_language_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """Calculate language usage distribution"""
        language_counts = {}
        
        for languages_list in df['languages_used']:
            if languages_list:
                for lang in languages_list:
                    language_counts[lang] = language_counts.get(lang, 0) + 1
        
        return language_counts
    
    def _calculate_cultural_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """Calculate cultural context distribution"""
        return df['cultural_context'].value_counts().to_dict()
    
    def _calculate_peak_usage_hours(self, df: pd.DataFrame) -> Dict[str, int]:
        """Calculate peak usage hours"""
        df['hour'] = df['start_time'].dt.hour
        return df['hour'].value_counts().to_dict()
    
    def _generate_usage_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate usage insights"""
        insights = []
        
        # Check for usage patterns
        avg_messages = df['messages_exchanged'].mean()
        if avg_messages > 10:
            insights.append("Users are engaging in lengthy conversations")
        
        # Check for language diversity
        language_dist = self._calculate_language_distribution(df)
        if len(language_dist) > 5:
            insights.append("Strong multilingual usage across diverse languages")
        
        # Check for crisis detection rate
        crisis_rate = df['crisis_detected'].mean()
        if crisis_rate > 0.05:
            insights.append("Higher than average crisis detection rate - good safety net")
        
        return insights
    
    def _generate_usage_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate usage recommendations"""
        recommendations = []
        
        # Analyze usage patterns
        peak_hours = self._calculate_peak_usage_hours(df)
        if peak_hours:
            peak_hour = max(peak_hours.items(), key=lambda x: x[1])[0]
            recommendations.append(f"Peak usage is at {peak_hour}:00 - consider staff scheduling")
        
        # Analyze language needs
        language_dist = self._calculate_language_distribution(df)
        if len(language_dist) > 10:
            recommendations.append("Consider expanding language support teams")
        
        return recommendations
    
    def _analyze_crisis_severity(self, crisis_events: List[Dict]) -> Dict[str, int]:
        """Analyze crisis severity distribution"""
        severity_counts = {}
        for event in crisis_events:
            severity = event.get('severity', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return severity_counts
    
    def _analyze_crisis_timing(self, crisis_events: List[Dict]) -> Dict[str, Any]:
        """Analyze crisis timing patterns"""
        hours = [event.get('timestamp', datetime.now()).hour for event in crisis_events]
        return {
            'peak_hours': pd.Series(hours).value_counts().to_dict(),
            'average_hour': np.mean(hours)
        }
    
    def _analyze_crisis_cultural_context(self, crisis_events: List[Dict]) -> Dict[str, int]:
        """Analyze crisis cultural context"""
        cultural_counts = {}
        for event in crisis_events:
            context = event.get('cultural_context', 'unknown')
            cultural_counts[context] = cultural_counts.get(context, 0) + 1
        return cultural_counts
    
    def _analyze_intervention_effectiveness(self, crisis_events: List[Dict]) -> Dict[str, float]:
        """Analyze intervention effectiveness"""
        # This would require follow-up data
        return {
            'immediate_response_rate': 0.95,  # Placeholder
            'follow_up_completion_rate': 0.75,  # Placeholder
            'user_satisfaction_score': 4.2  # Placeholder
        }
    
    def _generate_crisis_insights(self, crisis_events: List[Dict]) -> List[str]:
        """Generate crisis insights"""
        insights = []
        
        if len(crisis_events) > 0:
            insights.append(f"Detected {len(crisis_events)} crisis events requiring attention")
        
        # Analyze timing patterns
        timing = self._analyze_crisis_timing(crisis_events)
        if timing['peak_hours']:
            peak_hour = max(timing['peak_hours'].items(), key=lambda x: x[1])[0]
            insights.append(f"Crisis events peak at {peak_hour}:00")
        
        return insights
    
    def _generate_crisis_recommendations(self, crisis_events: List[Dict]) -> List[str]:
        """Generate crisis recommendations"""
        recommendations = []
        
        if len(crisis_events) > 0:
            recommendations.append("Ensure crisis response protocols are regularly updated")
            recommendations.append("Consider additional training for crisis intervention")
        
        return recommendations
    
    async def _update_mood_analytics(self, mood_entry: MoodEntry):
        """Update real-time mood analytics"""
        # This would update real-time dashboards
        pass
    
    async def _update_progress_analytics(self, progress_metric: ProgressMetric):
        """Update real-time progress analytics"""
        # This would update real-time dashboards
        pass
    
    async def _update_usage_analytics(self, usage_metric: UsageMetric):
        """Update real-time usage analytics"""
        # This would update real-time dashboards
        pass
    
    async def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """
        Get data for analytics dashboard
        
        Returns:
            Dict[str, Any]: Dashboard data
        """
        try:
            # Get recent reports
            mood_report = await self.generate_mood_report(days=7)
            progress_report = await self.generate_progress_report(days=7)
            usage_report = await self.generate_usage_report(days=7)
            
            return {
                'mood_summary': mood_report,
                'progress_summary': progress_report,
                'usage_summary': usage_report,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Dashboard data generation failed: {e}")
            raise AnalyticsError(f"Dashboard data generation failed: {e}", "ANALYTICS_008")
    
    async def cleanup(self):
        """Cleanup analytics resources"""
        try:
            # Clear caches
            self.analytics_cache.clear()
            self.metrics_buffer.clear()
            
            logger.info("Analytics cleanup completed")
            
        except Exception as e:
            logger.error(f"Analytics cleanup failed: {e}")
    
    def get_analytics_statistics(self) -> Dict[str, Any]:
        """Get analytics engine statistics"""
        return {
            'cached_reports': len(self.analytics_cache),
            'buffered_metrics': len(self.metrics_buffer),
            'supported_analytics': [analytics_type.value for analytics_type in AnalyticsType]
        }

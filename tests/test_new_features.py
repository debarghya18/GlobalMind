"""
Integration tests for GlobalMind new features
Tests voice processing, SMS, analytics, and AI model integration
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import pandas as pd

# Import modules to test
from src.nlp.voice_processor import VoiceProcessor
from src.nlp.sms_handler import SMSHandler
from src.monitoring.analytics import AdvancedAnalytics, MoodEntry, MoodLevel, ProgressMetric, UsageMetric
from src.models.therapy_models import TherapyModels
from src.cultural.adapter import CulturalAdapter
from src.core.exceptions import VoiceProcessingError, SMSServiceError, AnalyticsError


class TestVoiceProcessor:
    """Test voice processing functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.supported_languages = ['en', 'es', 'fr', 'de']
        self.voice_processor = VoiceProcessor(self.supported_languages)
    
    def test_voice_processor_initialization(self):
        """Test voice processor initialization"""
        assert self.voice_processor.supported_languages == self.supported_languages
        assert self.voice_processor.recognizer is not None
        assert len(self.voice_processor.speech_recognition_languages) > 0
    
    @pytest.mark.asyncio
    async def test_text_to_speech(self):
        """Test text-to-speech conversion"""
        with patch('gtts.gTTS') as mock_gtts:
            mock_gtts.return_value.save = Mock()
            
            result = await self.voice_processor.text_to_speech("Hello world", "en")
            assert result is not None
            assert result.endswith('.mp3')
            mock_gtts.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_therapeutic_audio_generation(self):
        """Test therapeutic audio generation"""
        with patch.object(self.voice_processor, 'text_to_speech') as mock_tts:
            mock_tts.return_value = "/tmp/test.mp3"
            
            with patch.object(self.voice_processor, '_apply_therapeutic_audio_processing') as mock_process:
                mock_process.return_value = "/tmp/processed.mp3"
                
                result = await self.voice_processor.generate_therapeutic_audio(
                    "You are doing great", "en", "calm"
                )
                assert result == "/tmp/processed.mp3"
    
    @pytest.mark.asyncio
    async def test_voice_statistics(self):
        """Test voice statistics retrieval"""
        stats = await self.voice_processor.get_voice_statistics()
        assert 'supported_languages' in stats
        assert 'microphone_available' in stats
        assert 'is_listening' in stats
        assert stats['supported_languages'] == 4
    
    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test voice processor cleanup"""
        await self.voice_processor.cleanup()
        assert not self.voice_processor.is_listening


class TestSMSHandler:
    """Test SMS handling functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_config = Mock()
        self.mock_config.account_sid = "test_sid"
        self.mock_config.auth_token = "test_token"
        self.mock_config.from_number = "+1234567890"
    
    def test_sms_handler_initialization(self):
        """Test SMS handler initialization"""
        with patch('twilio.rest.Client') as mock_client:
            sms_handler = SMSHandler(self.mock_config)
            assert sms_handler.config == self.mock_config
            mock_client.assert_called_once_with("test_sid", "test_token")
    
    def test_send_sms(self):
        """Test SMS sending"""
        with patch('twilio.rest.Client') as mock_client:
            mock_client.return_value.messages.create = Mock(return_value=Mock())
            
            sms_handler = SMSHandler(self.mock_config)
            result = sms_handler.send_sms("+1987654321", "Test message")
            
            assert result is True
            mock_client.return_value.messages.create.assert_called_once()
    
    def test_phone_number_validation(self):
        """Test phone number validation"""
        assert SMSHandler.validate_phone_number("1234567890") is True
        assert SMSHandler.validate_phone_number("123") is False
        assert SMSHandler.validate_phone_number("abcdefghij") is False


class TestAdvancedAnalytics:
    """Test advanced analytics functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_database = Mock()
        self.analytics = AdvancedAnalytics(self.mock_database)
    
    @pytest.mark.asyncio
    async def test_mood_tracking(self):
        """Test mood entry tracking"""
        mood_entry = MoodEntry(
            timestamp=datetime.now(),
            mood_level=MoodLevel.GOOD,
            notes="Feeling positive today",
            user_id="test_user"
        )
        
        self.mock_database.store_mood_entry = Mock(return_value=True)
        
        result = await self.analytics.track_mood(mood_entry)
        assert result is True
        self.mock_database.store_mood_entry.assert_called_once_with(mood_entry)
    
    @pytest.mark.asyncio
    async def test_progress_tracking(self):
        """Test progress metric tracking"""
        progress_metric = ProgressMetric(
            metric_name="anxiety_level",
            value=3.5,
            timestamp=datetime.now(),
            user_id="test_user"
        )
        
        self.mock_database.store_progress_metric = Mock(return_value=True)
        
        result = await self.analytics.track_progress(progress_metric)
        assert result is True
        self.mock_database.store_progress_metric.assert_called_once_with(progress_metric)
    
    @pytest.mark.asyncio
    async def test_usage_tracking(self):
        """Test usage metric tracking"""
        usage_metric = UsageMetric(
            session_id="test_session",
            user_id="test_user",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=30),
            messages_exchanged=15,
            languages_used=["en", "es"],
            cultural_context="western"
        )
        
        self.mock_database.store_usage_metric = Mock(return_value=True)
        
        result = await self.analytics.track_usage(usage_metric)
        assert result is True
        self.mock_database.store_usage_metric.assert_called_once_with(usage_metric)
    
    @pytest.mark.asyncio
    async def test_mood_report_generation(self):
        """Test mood report generation"""
        mock_mood_entries = [
            MoodEntry(datetime.now() - timedelta(days=1), MoodLevel.GOOD),
            MoodEntry(datetime.now() - timedelta(days=2), MoodLevel.NEUTRAL),
            MoodEntry(datetime.now() - timedelta(days=3), MoodLevel.VERY_GOOD)
        ]
        
        self.mock_database.get_mood_entries = Mock(return_value=mock_mood_entries)
        
        report = await self.analytics.generate_mood_report(user_id="test_user", days=7)
        
        assert 'statistics' in report
        assert 'insights' in report
        assert 'recommendations' in report
        assert report['statistics']['total_entries'] == 3
    
    @pytest.mark.asyncio
    async def test_dashboard_data(self):
        """Test analytics dashboard data generation"""
        # Mock all required methods
        self.mock_database.get_mood_entries = Mock(return_value=[])
        self.mock_database.get_progress_metrics = Mock(return_value=[])
        self.mock_database.get_usage_metrics = Mock(return_value=[])
        
        dashboard_data = await self.analytics.get_analytics_dashboard_data()
        
        assert 'mood_summary' in dashboard_data
        assert 'progress_summary' in dashboard_data
        assert 'usage_summary' in dashboard_data
        assert 'last_updated' in dashboard_data


class TestTherapyModels:
    """Test therapy models functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_config = Mock()
        self.therapy_models = TherapyModels(self.mock_config)
    
    def test_therapy_models_initialization(self):
        """Test therapy models initialization"""
        assert self.therapy_models.config == self.mock_config
        assert len(self.therapy_models.therapeutic_frameworks) > 0
        assert 'western_cbt' in self.therapy_models.therapeutic_frameworks
        assert 'eastern_mindfulness' in self.therapy_models.therapeutic_frameworks
    
    @pytest.mark.asyncio
    async def test_response_generation(self):
        """Test therapeutic response generation"""
        cultural_context = {
            'therapeutic_approach': 'western_cbt',
            'cultural_region': 'western',
            'communication_style': 'direct'
        }
        
        response = await self.therapy_models.generate_response(
            "I'm feeling anxious",
            cultural_context
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_crisis_response_generation(self):
        """Test crisis response generation"""
        cultural_context = {
            'cultural_region': 'western',
            'language': 'en'
        }
        
        response = await self.therapy_models.generate_crisis_response(
            "I want to hurt myself",
            cultural_context
        )
        
        assert isinstance(response, str)
        assert "988" in response  # Crisis hotline number
        assert "IMMEDIATE HELP" in response
    
    def test_theme_analysis(self):
        """Test input theme analysis"""
        themes = self.therapy_models._analyze_input_themes("I'm feeling very anxious and worried")
        assert 'anxiety' in themes
        
        themes = self.therapy_models._analyze_input_themes("Hello, how are you?")
        assert 'greeting' in themes
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test therapy models health check"""
        result = await self.therapy_models.health_check()
        assert isinstance(result, bool)
    
    def test_model_statistics(self):
        """Test model statistics retrieval"""
        stats = self.therapy_models.get_model_statistics()
        assert 'therapeutic_frameworks' in stats
        assert 'total_responses' in stats
        assert stats['therapeutic_frameworks'] > 0


class TestCulturalAdapter:
    """Test cultural adaptation functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.cultural_adapter = CulturalAdapter([], {})
    
    def test_cultural_adapter_initialization(self):
        """Test cultural adapter initialization"""
        assert len(self.cultural_adapter.metaphors_database) > 0
        assert 'western' in self.cultural_adapter.metaphors_database
        assert 'eastern' in self.cultural_adapter.metaphors_database
        assert 'african' in self.cultural_adapter.metaphors_database
        assert 'latin' in self.cultural_adapter.metaphors_database
    
    @pytest.mark.asyncio
    async def test_cultural_context_generation(self):
        """Test cultural context generation"""
        user_profile = {}
        language = 'es'
        
        context = await self.cultural_adapter.get_context(user_profile, language)
        
        assert 'cultural_region' in context
        assert 'language' in context
        assert 'communication_style' in context
        assert 'therapeutic_approach' in context
        assert context['cultural_region'] == 'latin'
        assert context['language'] == 'es'
    
    @pytest.mark.asyncio
    async def test_response_adaptation(self):
        """Test response cultural adaptation"""
        response = "You should try to feel better"
        cultural_context = {
            'cultural_region': 'eastern',
            'communication_style': 'indirect'
        }
        
        adapted_response = await self.cultural_adapter.adapt_response(response, cultural_context)
        
        assert adapted_response != response
        assert 'perhaps' in adapted_response.lower() or 'might' in adapted_response.lower()
    
    @pytest.mark.asyncio
    async def test_emergency_resources(self):
        """Test culturally appropriate emergency resources"""
        cultural_context = {
            'cultural_region': 'african',
            'language': 'sw'
        }
        
        resources = await self.cultural_adapter.get_emergency_resources(cultural_context)
        
        assert len(resources) > 0
        assert any(resource['type'] == 'crisis_hotline' for resource in resources)
        assert any(resource['type'] == 'community_elder' for resource in resources)
    
    def test_cultural_statistics(self):
        """Test cultural statistics retrieval"""
        stats = self.cultural_adapter.get_cultural_statistics()
        assert 'supported_regions' in stats
        assert 'therapeutic_approaches' in stats
        assert stats['supported_regions'] > 0


class TestIntegration:
    """Integration tests for combined functionality"""
    
    @pytest.mark.asyncio
    async def test_full_therapeutic_conversation_flow(self):
        """Test complete therapeutic conversation flow"""
        # Setup components
        cultural_adapter = CulturalAdapter([], {})
        therapy_models = TherapyModels(Mock())
        
        # Simulate user input
        user_input = "I'm feeling very anxious about work"
        user_profile = {'cultural_background': 'western'}
        language = 'en'
        
        # Get cultural context
        cultural_context = await cultural_adapter.get_context(user_profile, language)
        
        # Generate response
        response = await therapy_models.generate_response(user_input, cultural_context)
        
        # Adapt response culturally
        adapted_response = await cultural_adapter.adapt_response(response, cultural_context)
        
        assert isinstance(adapted_response, str)
        assert len(adapted_response) > 0
        assert cultural_context['cultural_region'] == 'western'
        assert cultural_context['therapeutic_approach'] == 'western_cbt'
    
    @pytest.mark.asyncio
    async def test_crisis_detection_and_response_flow(self):
        """Test crisis detection and response flow"""
        # Setup components
        cultural_adapter = CulturalAdapter([], {})
        therapy_models = TherapyModels(Mock())
        
        # Simulate crisis input
        crisis_input = "I want to end my life"
        user_profile = {}
        language = 'en'
        
        # Get cultural context
        cultural_context = await cultural_adapter.get_context(user_profile, language)
        
        # Generate crisis response
        crisis_response = await therapy_models.generate_crisis_response(crisis_input, cultural_context)
        
        # Verify crisis response contains emergency information
        assert "988" in crisis_response
        assert "IMMEDIATE HELP" in crisis_response
        assert "Crisis" in crisis_response
    
    @pytest.mark.asyncio
    async def test_analytics_mood_progress_integration(self):
        """Test analytics integration with mood and progress tracking"""
        # Setup analytics
        mock_database = Mock()
        analytics = AdvancedAnalytics(mock_database)
        
        # Create test data
        mood_entries = [
            MoodEntry(datetime.now() - timedelta(days=i), MoodLevel.GOOD if i % 2 == 0 else MoodLevel.NEUTRAL)
            for i in range(10)
        ]
        
        progress_metrics = [
            ProgressMetric("anxiety_level", 4.0 - i * 0.2, datetime.now() - timedelta(days=i))
            for i in range(10)
        ]
        
        # Mock database responses
        mock_database.get_mood_entries = Mock(return_value=mood_entries)
        mock_database.get_progress_metrics = Mock(return_value=progress_metrics)
        mock_database.get_usage_metrics = Mock(return_value=[])
        
        # Generate comprehensive dashboard
        dashboard_data = await analytics.get_analytics_dashboard_data()
        
        assert 'mood_summary' in dashboard_data
        assert 'progress_summary' in dashboard_data
        assert dashboard_data['mood_summary']['statistics']['total_entries'] == 10
        assert dashboard_data['progress_summary']['metrics_analysis']['anxiety_level']['improvement'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

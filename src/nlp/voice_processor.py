"""
Voice processing module for GlobalMind
Handles speech recognition and text-to-speech functionality
"""

import asyncio
import os
import tempfile
from typing import Dict, Any, Optional, List
from loguru import logger
import speech_recognition as sr
from gtts import gTTS
import pydub
from pydub import AudioSegment
from pydub.playback import play
import wave
import io
import threading
import queue

from ..core.exceptions import VoiceProcessingError


class VoiceProcessor:
    """Handles voice input and output for the therapy assistant"""
    
    def __init__(self, supported_languages: List[str]):
        """
        Initialize voice processor
        
        Args:
            supported_languages: List of supported language codes
        """
        self.supported_languages = supported_languages
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Language mapping for speech recognition
        self.speech_recognition_languages = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-BR',
            'ru': 'ru-RU',
            'zh': 'zh-CN',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'ar': 'ar-SA',
            'hi': 'hi-IN',
            'th': 'th-TH',
            'vi': 'vi-VN'
        }
        
        # Initialize microphone
        self._initialize_microphone()
        
        logger.info(f"Voice processor initialized with {len(supported_languages)} languages")
    
    def _initialize_microphone(self):
        """Initialize microphone for speech recognition"""
        try:
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
            logger.info("Microphone initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to initialize microphone: {e}")
            self.microphone = None
    
    async def speech_to_text(self, language: str = 'en', timeout: int = 30) -> Optional[str]:
        """
        Convert speech to text
        
        Args:
            language: Language code for recognition
            timeout: Timeout in seconds
            
        Returns:
            str: Recognized text or None if failed
        """
        try:
            if not self.microphone:
                raise VoiceProcessingError("Microphone not available", "VOICE_001")
            
            # Get speech recognition language
            speech_lang = self.speech_recognition_languages.get(language, 'en-US')
            
            logger.info(f"Listening for speech in {speech_lang}...")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            logger.info("Processing speech...")
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=speech_lang)
            
            logger.info(f"Speech recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("Speech recognition timed out")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition request error: {e}")
            raise VoiceProcessingError(f"Speech recognition failed: {e}", "VOICE_002")
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            raise VoiceProcessingError(f"Speech recognition failed: {e}", "VOICE_002")
    
    async def text_to_speech(self, text: str, language: str = 'en') -> Optional[str]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            language: Language code
            
        Returns:
            str: Path to generated audio file
        """
        try:
            # Validate language
            if language not in self.supported_languages:
                logger.warning(f"Language {language} not supported, using English")
                language = 'en'
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_path = tmp_file.name
            
            # Generate speech
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(temp_path)
            
            logger.info(f"Text-to-speech generated: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            raise VoiceProcessingError(f"Text-to-speech failed: {e}", "VOICE_003")
    
    async def play_audio(self, audio_path: str) -> bool:
        """
        Play audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            bool: True if successful
        """
        try:
            # Load and play audio
            audio = AudioSegment.from_file(audio_path)
            play(audio)
            
            # Clean up temporary file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
            return False
    
    async def start_continuous_listening(self, language: str = 'en', callback=None):
        """
        Start continuous listening for voice input
        
        Args:
            language: Language code
            callback: Callback function for recognized text
        """
        try:
            if not self.microphone:
                raise VoiceProcessingError("Microphone not available", "VOICE_001")
            
            self.is_listening = True
            speech_lang = self.speech_recognition_languages.get(language, 'en-US')
            
            def listen_worker():
                while self.is_listening:
                    try:
                        with self.microphone as source:
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        
                        # Process in background
                        threading.Thread(
                            target=self._process_audio,
                            args=(audio, speech_lang, callback)
                        ).start()
                        
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Continuous listening error: {e}")
                        break
            
            # Start listening in background thread
            listening_thread = threading.Thread(target=listen_worker)
            listening_thread.daemon = True
            listening_thread.start()
            
            logger.info("Continuous listening started")
            
        except Exception as e:
            logger.error(f"Failed to start continuous listening: {e}")
            raise VoiceProcessingError(f"Continuous listening failed: {e}", "VOICE_004")
    
    def _process_audio(self, audio, language, callback):
        """Process audio in background thread"""
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            if callback and text:
                callback(text)
        except:
            pass  # Ignore errors in background processing
    
    async def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        logger.info("Continuous listening stopped")
    
    async def process_audio_file(self, audio_path: str, language: str = 'en') -> Optional[str]:
        """
        Process audio file for speech recognition
        
        Args:
            audio_path: Path to audio file
            language: Language code
            
        Returns:
            str: Recognized text or None
        """
        try:
            # Load audio file
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
            
            # Get speech recognition language
            speech_lang = self.speech_recognition_languages.get(language, 'en-US')
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=speech_lang)
            
            logger.info(f"Audio file processed: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio in file")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition request error: {e}")
            raise VoiceProcessingError(f"Audio file processing failed: {e}", "VOICE_005")
        except Exception as e:
            logger.error(f"Audio file processing error: {e}")
            raise VoiceProcessingError(f"Audio file processing failed: {e}", "VOICE_005")
    
    async def generate_therapeutic_audio(
        self, 
        text: str, 
        language: str = 'en', 
        voice_style: str = 'calm'
    ) -> Optional[str]:
        """
        Generate therapeutic audio with appropriate tone
        
        Args:
            text: Text to convert
            language: Language code
            voice_style: Voice style (calm, encouraging, etc.)
            
        Returns:
            str: Path to generated audio file
        """
        try:
            # Adjust text for therapeutic tone
            therapeutic_text = self._adjust_text_for_therapy(text, voice_style)
            
            # Generate audio
            audio_path = await self.text_to_speech(therapeutic_text, language)
            
            if audio_path:
                # Apply audio processing for therapeutic effect
                processed_path = await self._apply_therapeutic_audio_processing(audio_path)
                return processed_path
            
            return audio_path
            
        except Exception as e:
            logger.error(f"Therapeutic audio generation error: {e}")
            raise VoiceProcessingError(f"Therapeutic audio generation failed: {e}", "VOICE_006")
    
    def _adjust_text_for_therapy(self, text: str, style: str) -> str:
        """Adjust text for therapeutic tone"""
        if style == 'calm':
            # Add pauses for calming effect
            text = text.replace('.', '... ')
            text = text.replace(',', ', ')
        elif style == 'encouraging':
            # Add emphasis
            text = text.replace('you can', 'you CAN')
            text = text.replace('you are', 'you ARE')
        
        return text
    
    async def _apply_therapeutic_audio_processing(self, audio_path: str) -> str:
        """Apply audio processing for therapeutic effect"""
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Apply therapeutic processing
            # Slow down slightly for calming effect
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * 0.95)
            })
            
            # Normalize volume
            audio = audio.normalize()
            
            # Create new temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                processed_path = tmp_file.name
            
            # Export processed audio
            audio.export(processed_path, format="mp3")
            
            # Clean up original file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return processed_path
            
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return audio_path  # Return original if processing fails
    
    async def get_voice_statistics(self) -> Dict[str, Any]:
        """Get voice processing statistics"""
        return {
            'supported_languages': len(self.supported_languages),
            'microphone_available': self.microphone is not None,
            'is_listening': self.is_listening,
            'speech_recognition_languages': len(self.speech_recognition_languages)
        }
    
    async def test_voice_components(self) -> Dict[str, bool]:
        """Test voice processing components"""
        results = {
            'microphone': False,
            'speech_recognition': False,
            'text_to_speech': False
        }
        
        try:
            # Test microphone
            if self.microphone:
                results['microphone'] = True
            
            # Test speech recognition (if microphone available)
            if self.microphone:
                try:
                    # Quick test with short timeout
                    test_text = await self.speech_to_text(timeout=2)
                    results['speech_recognition'] = True
                except:
                    pass
            
            # Test text-to-speech
            try:
                test_audio = await self.text_to_speech("Test", "en")
                if test_audio and os.path.exists(test_audio):
                    results['text_to_speech'] = True
                    os.remove(test_audio)
            except:
                pass
                
        except Exception as e:
            logger.error(f"Voice component test error: {e}")
        
        return results
    
    async def cleanup(self):
        """Cleanup voice processor resources"""
        try:
            await self.stop_continuous_listening()
            logger.info("Voice processor cleanup completed")
        except Exception as e:
            logger.error(f"Voice processor cleanup error: {e}")
    
    def get_supported_speech_languages(self) -> List[str]:
        """Get list of supported speech recognition languages"""
        return list(self.speech_recognition_languages.keys())
    
    def is_voice_input_available(self) -> bool:
        """Check if voice input is available"""
        return self.microphone is not None
    
    def is_voice_output_available(self) -> bool:
        """Check if voice output is available"""
        return True  # gTTS is always available if internet connection exists

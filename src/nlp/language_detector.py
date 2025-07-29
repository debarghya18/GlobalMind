"""
Language detection service for GlobalMind
Provides multilingual language detection capabilities
"""

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger
import langdetect
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException

from ..core.exceptions import TranslationError


class LanguageDetector:
    """Detects language from text input"""
    
    def __init__(self, supported_languages: List[str]):
        """
        Initialize language detector
        
        Args:
            supported_languages: List of supported language codes
        """
        self.supported_languages = supported_languages
        self.language_cache = {}
        
        # Set seed for consistent results
        langdetect.detector_factory.seed = 0
        
        logger.info(f"Language detector initialized with {len(supported_languages)} languages")
    
    async def detect(self, text: str) -> str:
        """
        Detect language from text
        
        Args:
            text: Input text to analyze
            
        Returns:
            str: Detected language code
        """
        try:
            if not text or len(text.strip()) < 3:
                return 'en'  # Default to English for short texts
            
            # Check cache first
            text_hash = hash(text)
            if text_hash in self.language_cache:
                return self.language_cache[text_hash]
            
            # Detect language
            detected_lang = detect(text)
            
            # Validate against supported languages
            if detected_lang not in self.supported_languages:
                logger.warning(f"Detected language '{detected_lang}' not supported, using fallback")
                detected_lang = 'en'  # Fallback to English
            
            # Cache result
            self.language_cache[text_hash] = detected_lang
            
            logger.debug(f"Detected language: {detected_lang}")
            return detected_lang
            
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English")
            return 'en'
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            raise TranslationError(f"Language detection failed: {e}", "TRANS_001")
    
    async def detect_with_confidence(self, text: str) -> Tuple[str, float]:
        """
        Detect language with confidence score
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple[str, float]: (language_code, confidence_score)
        """
        try:
            if not text or len(text.strip()) < 3:
                return 'en', 0.5
            
            # Get language probabilities
            lang_probs = detect_langs(text)
            
            if not lang_probs:
                return 'en', 0.5
            
            # Get the most likely language
            top_lang = lang_probs[0]
            detected_lang = top_lang.lang
            confidence = top_lang.prob
            
            # Validate against supported languages
            if detected_lang not in self.supported_languages:
                logger.warning(f"Detected language '{detected_lang}' not supported, using fallback")
                detected_lang = 'en'
                confidence = 0.5
            
            logger.debug(f"Detected language: {detected_lang} (confidence: {confidence:.2f})")
            return detected_lang, confidence
            
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English")
            return 'en', 0.5
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            raise TranslationError(f"Language detection failed: {e}", "TRANS_001")
    
    async def detect_multiple_languages(self, text: str, threshold: float = 0.1) -> List[Tuple[str, float]]:
        """
        Detect multiple possible languages
        
        Args:
            text: Input text to analyze
            threshold: Minimum confidence threshold
            
        Returns:
            List[Tuple[str, float]]: List of (language_code, confidence) tuples
        """
        try:
            if not text or len(text.strip()) < 3:
                return [('en', 0.5)]
            
            # Get language probabilities
            lang_probs = detect_langs(text)
            
            # Filter by threshold and supported languages
            results = []
            for lang_prob in lang_probs:
                if (lang_prob.prob >= threshold and 
                    lang_prob.lang in self.supported_languages):
                    results.append((lang_prob.lang, lang_prob.prob))
            
            if not results:
                return [('en', 0.5)]
            
            logger.debug(f"Detected languages: {results}")
            return results
            
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English")
            return [('en', 0.5)]
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            raise TranslationError(f"Language detection failed: {e}", "TRANS_001")
    
    async def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported
        
        Args:
            language_code: Language code to check
            
        Returns:
            bool: True if supported
        """
        return language_code in self.supported_languages
    
    async def get_language_name(self, language_code: str) -> str:
        """
        Get human-readable language name
        
        Args:
            language_code: Language code
            
        Returns:
            str: Language name
        """
        # Language code to name mapping
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Filipino',
            'sw': 'Swahili',
            'am': 'Amharic',
            'yo': 'Yoruba',
            'ig': 'Igbo',
            'ha': 'Hausa',
            'zu': 'Zulu',
            'xh': 'Xhosa',
            'af': 'Afrikaans',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            'fa': 'Persian',
            'he': 'Hebrew',
            'tr': 'Turkish',
            'pl': 'Polish',
            'uk': 'Ukrainian',
            'cs': 'Czech',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sr': 'Serbian',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'fi': 'Finnish',
            'da': 'Danish',
            'no': 'Norwegian',
            'sv': 'Swedish',
            'is': 'Icelandic'
        }
        
        return language_names.get(language_code, language_code.upper())
    
    async def batch_detect(self, texts: List[str]) -> List[str]:
        """
        Detect languages for multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List[str]: List of detected language codes
        """
        try:
            results = []
            
            for text in texts:
                lang = await self.detect(text)
                results.append(lang)
            
            return results
            
        except Exception as e:
            logger.error(f"Batch language detection failed: {e}")
            raise TranslationError(f"Batch language detection failed: {e}", "TRANS_001")
    
    async def health_check(self) -> bool:
        """
        Perform health check on language detector
        
        Returns:
            bool: True if healthy
        """
        try:
            # Test detection with a simple English phrase
            test_result = await self.detect("Hello, how are you?")
            return test_result == 'en'
            
        except Exception as e:
            logger.error(f"Language detector health check failed: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get language detector statistics
        
        Returns:
            Dict[str, Any]: Statistics
        """
        return {
            'supported_languages': len(self.supported_languages),
            'cache_size': len(self.language_cache),
            'languages': self.supported_languages
        }
    
    def clear_cache(self):
        """Clear language detection cache"""
        self.language_cache.clear()
        logger.info("Language detection cache cleared")

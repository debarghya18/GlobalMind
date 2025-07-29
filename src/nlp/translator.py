"""
Multilingual translation service for GlobalMind
Uses translation models and external APIs for translation
"""

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger
from transformers import MarianMTModel, MarianTokenizer
from deep_translator import GoogleTranslator

from ..core.exceptions import TranslationError
from ..core.config import ModelsConfig


class MultilingualTranslator:
    """Provides translation services using AI models and APIs"""
    
    def __init__(self, model_name: str, supported_languages: List[str]):
        """
        Initialize the translator
        
        Args:
            model_name: Name of the translation model
            supported_languages: Supported language codes
        """
        self.supported_languages = supported_languages
        self.model_name = model_name  # Example: 'Helsinki-NLP/opus-mt-en-{language_code}'
        self.models = {}
        self.tokenizers = {}
        
        self._init_models()
    
    def _init_models(self):
        """Initialize translation models"""
        try:
            # Load translation models for each supported language
            for lang in self.supported_languages:
                model_key = f"en-{lang}"
                if model_key not in self.models:
                    model = MarianMTModel.from_pretrained(f"Helsinki-NLP/opus-mt-en-{lang}")
                    tokenizer = MarianTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-en-{lang}")
                    self.models[model_key] = model
                    self.tokenizers[model_key] = tokenizer
                    logger.info(f"Loaded translation model for {lang}")
            
            logger.info("Translation models initialized successfully")
        except Exception as e:
            logger.error(f"Model initialization failed: {e}")
            raise TranslationError(f"Model loading failed: {e}", "MODEL_001")

    async def translate(self, text: str, target_lang: str) -> str:
        """
        Translate text to the target language
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            str: Translated text
        """
        try:
            if target_lang not in self.supported_languages:
                raise TranslationError(f"Unsupported language: {target_lang}", "TRANS_002")
            
            model_key = f"en-{target_lang}"
            model = self.models.get(model_key)
            tokenizer = self.tokenizers.get(model_key)

            if not model or not tokenizer:
                raise TranslationError(f"Translation model not loaded for {target_lang}", "MODEL_003")

            # Tokenize source text
            tokenized_text = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')

            # Generate translation
            translated = model.generate(**tokenized_text)
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            
            logger.debug(f"Translated text: {translated_text}")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise TranslationError(f"Translation failed: {e}", "TRANS_003")
    
    async def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages
        
        Returns:
            List[str]: Supported language codes
        """
        return self.supported_languages

    async def health_check(self) -> bool:
        """
        Perform health check on translation service
        
        Returns:
            bool: True if healthy
        """
        try:
            # Test translation with a simple phrase
            test_result = await self.translate("Hello, how are you?", "es")
            return test_result.lower().startswith("hola")
        except Exception as e:
            logger.error(f"Translation service health check failed: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get translation service statistics
        
        Returns:
            Dict[str, Any]: Statistics
        """
        return {
            'supported_languages': len(self.supported_languages),
            'loaded_models': len(self.models),
        }

    async def translate_batch(self, texts: List[str], target_lang: str) -> List[str]:
        """
        Translate a batch of texts to the target language
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
        
        Returns:
            List[str]: Translated texts
        """
        try:
            if target_lang not in self.supported_languages:
                raise TranslationError(f"Unsupported language: {target_lang}", "TRANS_002")
            
            model_key = f"en-{target_lang}"
            model = self.models.get(model_key)
            tokenizer = self.tokenizers.get(model_key)

            if not model or not tokenizer:
                raise TranslationError(f"Translation model not loaded for {target_lang}", "MODEL_003")

            # Tokenize source texts
            tokenized_texts = tokenizer.prepare_seq2seq_batch(texts, return_tensors='pt', padding=True)

            # Generate translations
            translated_outputs = model.generate(**tokenized_texts)
            
            translated_texts = [tokenizer.decode(t, skip_special_tokens=True) for t in translated_outputs]
            logger.debug(f"Translated batch texts: {translated_texts}")

            return translated_texts
        except Exception as e:
            logger.error(f"Batch translation failed: {e}")
            raise TranslationError(f"Batch translation failed: {e}", "TRANS_003")

    async def switch_language(self, current_lang: str, new_lang: str, text: str) -> str:
        """
        Switch language context without losing conversation context
        
        Args:
            current_lang: Current language of the text
            new_lang: New target language
            text: Text to be translated

        Returns:
            str: Translated text in the new language
        """
        try:
            # Translate from current to English first
            english_translation = await self.translate(text, "en")
            
            # Translate from English to the new language
            new_translation = await self.translate(english_translation, new_lang)
            
            logger.debug(f"Switch language translation: {new_translation}")
            return new_translation
        except Exception as e:
            logger.error(f"Language switch failed: {e}")
            raise TranslationError(f"Language switch failed: {e}", "TRANS_003")

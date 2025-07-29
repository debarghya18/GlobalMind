"""
Crisis detection AI model for GlobalMind
Identifies mental health emergencies and triggers appropriate responses
"""

import asyncio
import re
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
from datetime import datetime

from ..core.exceptions import CrisisDetectionError, ModelError


class CrisisDetector:
    """AI model for detecting mental health crises"""
    
    def __init__(self, model_name: str, crisis_keywords: List[str]):
        """
        Initialize crisis detector
        
        Args:
            model_name: Name of the crisis detection model
            crisis_keywords: List of crisis keywords
        """
        self.model_name = model_name
        self.crisis_keywords = crisis_keywords
        self.model_loaded = False
        
        # Crisis severity levels
        self.severity_levels = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8,
            'critical': 1.0
        }
        
        # Enhanced crisis patterns with severity weights
        self.crisis_patterns = {
            # Immediate danger - Critical level
            'immediate_danger': {
                'patterns': [
                    r'\b(?:kill|end|take)\s+(?:my|myself|my\s+life)\b',
                    r'\b(?:suicide|suicidal)\b',
                    r'\b(?:not\s+worth\s+living|no\s+reason\s+to\s+live)\b',
                    r'\b(?:want\s+to\s+die|wish\s+I\s+was\s+dead)\b',
                    r'\b(?:plan\s+to\s+(?:kill|hurt))\b',
                    r'\b(?:goodbye\s+(?:cruel\s+)?world)\b'
                ],
                'severity': 1.0,
                'urgency': 'immediate'
            },
            
            # Self-harm - High level
            'self_harm': {
                'patterns': [
                    r'\b(?:cut|cutting|harm)\s+(?:myself|my)\b',
                    r'\b(?:self\s*harm|self\s*injury)\b',
                    r'\b(?:hurt\s+myself)\b',
                    r'\b(?:razor|blade|pills)\b.*(?:hurt|harm|end)',
                    r'\b(?:overdose|too\s+many\s+pills)\b'
                ],
                'severity': 0.8,
                'urgency': 'high'
            },
            
            # Hopelessness - High level
            'hopelessness': {
                'patterns': [
                    r'\b(?:no\s+hope|hopeless|pointless)\b',
                    r'\b(?:nothing\s+matters|what\'s\s+the\s+point)\b',
                    r'\b(?:can\'t\s+(?:go\s+on|take\s+it)|unbearable)\b',
                    r'\b(?:trapped|no\s+way\s+out)\b',
                    r'\b(?:burden|waste\s+of\s+space)\b'
                ],
                'severity': 0.7,
                'urgency': 'high'
            },
            
            # Help seeking - Low level (positive indicator)
            'help_seeking': {
                'patterns': [
                    r'\b(?:need\s+help|please\s+help)\b',
                    r'\b(?:don\'t\s+know\s+what\s+to\s+do)\b',
                    r'\b(?:someone\s+to\s+talk\s+to)\b'
                ],
                'severity': 0.3,
                'urgency': 'low'
            }
        }
        
        logger.info("Crisis detector initialized")
    
    async def load_model(self):
        """Load crisis detection model"""
        try:
            logger.info("Loading crisis detection model...")
            await asyncio.sleep(0.5)
            self.model_loaded = True
            logger.info("Crisis detection model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load crisis detection model: {e}")
            raise ModelError(f"Crisis model loading failed: {e}", "MODEL_001")
    
    async def detect_crisis(self, text: str, cultural_context: Dict[str, Any] = None) -> float:
        """
        Detect crisis level in text
        
        Args:
            text: Input text to analyze
            cultural_context: Cultural context for adjustment
            
        Returns:
            float: Crisis level (0.0 to 1.0)
        """
        try:
            if not self.model_loaded:
                await self.load_model()
            
            if not text or not text.strip():
                return 0.0
            
            normalized_text = text.lower().strip()
            base_score = self._calculate_base_score(normalized_text)
            
            # Apply cultural adjustments if context provided
            if cultural_context:
                cultural_region = cultural_context.get('cultural_region', 'western')
                adjusted_score = self._apply_cultural_adjustment(base_score, cultural_region)
            else:
                adjusted_score = base_score
            
            final_score = max(0.0, min(1.0, adjusted_score))
            
            if final_score > 0.5:
                logger.warning(f"Crisis detected with score: {final_score:.2f}")
            
            return final_score
            
        except Exception as e:
            logger.error(f"Crisis detection failed: {e}")
            raise CrisisDetectionError(f"Crisis detection failed: {e}", "CRISIS_001")
    
    def _calculate_base_score(self, text: str) -> float:
        """Calculate base crisis score from text patterns"""
        max_score = 0.0
        
        for category, pattern_data in self.crisis_patterns.items():
            patterns = pattern_data['patterns']
            severity = pattern_data['severity']
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    max_score = max(max_score, severity)
        
        return max_score
    
    def _apply_cultural_adjustment(self, base_score: float, cultural_region: str) -> float:
        """Apply cultural adjustments to crisis score"""
        # Different cultures express distress differently
        cultural_factors = {
            'western': 1.0,     # Direct expression
            'eastern': 1.2,     # Often more indirect, may need sensitivity boost
            'african': 1.1,     # Community context important
            'latin': 1.0        # Generally expressive
        }
        
        factor = cultural_factors.get(cultural_region, 1.0)
        return min(1.0, base_score * factor)
    
    async def get_crisis_resources(self, crisis_level: float, cultural_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get appropriate crisis resources"""
        resources = [
            {
                'type': 'crisis_hotline',
                'name': 'National Crisis Lifeline',
                'phone': '988',
                'available': '24/7'
            },
            {
                'type': 'text_support',
                'name': 'Crisis Text Line',
                'text': 'Text HOME to 741741',
                'available': '24/7'
            }
        ]
        
        if crisis_level > 0.8:
            resources.insert(0, {
                'type': 'emergency',
                'name': 'Emergency Services',
                'phone': '911',
                'description': 'For immediate life-threatening emergencies'
            })
        
        return resources
    
    async def health_check(self) -> bool:
        """Perform health check on crisis detector"""
        try:
            test_score = await self.detect_crisis("I'm feeling sad today", {})
            return isinstance(test_score, float) and 0.0 <= test_score <= 1.0
        except Exception:
            return False
    
    async def cleanup(self):
        """Cleanup crisis detector resources"""
        self.model_loaded = False
        logger.info("Crisis detector cleanup completed")

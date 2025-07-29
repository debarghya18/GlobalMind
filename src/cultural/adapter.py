"""
Cultural Adaptation Engine for GlobalMind
Implements cultural intelligence and context-aware responses
"""

import asyncio
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
import json
import random
from pathlib import Path

from ..core.exceptions import CulturalAdaptationError


class CulturalAdapter:
    """Handles cultural adaptation for therapeutic responses"""
    
    def __init__(self, cultural_frameworks: List[str], regional_adaptations: Dict[str, List[str]]):
        """
        Initialize cultural adapter
        
        Args:
            cultural_frameworks: List of supported therapeutic frameworks
            regional_adaptations: Regional adaptation mappings
        """
        self.cultural_frameworks = cultural_frameworks
        self.regional_adaptations = regional_adaptations
        self.cultural_profiles = {}
        self.metaphors_database = {}
        self.therapeutic_approaches = {}
        
        self._load_cultural_data()
    
    def _load_cultural_data(self):
        """Load cultural data and profiles"""
        try:
            # Load cultural metaphors and expressions
            self.metaphors_database = {
                'western': {
                    'therapy_concepts': {
                        'healing': ['recovery', 'getting better', 'moving forward'],
                        'struggle': ['challenge', 'obstacle', 'hurdle'],
                        'growth': ['personal development', 'self-improvement', 'progress']
                    },
                    'communication_style': 'direct',
                    'family_involvement': 'low',
                    'spiritual_aspect': 'low'
                },
                'eastern': {
                    'therapy_concepts': {
                        'healing': ['harmony', 'balance', 'inner peace'],
                        'struggle': ['imbalance', 'disharmony', 'blocked energy'],
                        'growth': ['enlightenment', 'wisdom', 'cultivation']
                    },
                    'communication_style': 'indirect',
                    'family_involvement': 'high',
                    'spiritual_aspect': 'high'
                },
                'african': {
                    'therapy_concepts': {
                        'healing': ['restoration', 'wholeness', 'community healing'],
                        'struggle': ['disconnection', 'spiritual imbalance', 'ancestral grief'],
                        'growth': ['wisdom', 'community strength', 'ancestral guidance']
                    },
                    'communication_style': 'narrative',
                    'family_involvement': 'very_high',
                    'spiritual_aspect': 'very_high'
                },
                'latin': {
                    'therapy_concepts': {
                        'healing': ['fortaleza', 'familia support', 'resilience'],
                        'struggle': ['lucha', 'adversity', 'hardship'],
                        'growth': ['superación', 'achievement', 'family pride']
                    },
                    'communication_style': 'expressive',
                    'family_involvement': 'high',
                    'spiritual_aspect': 'high'
                }
            }
            
            # Load therapeutic approaches
            self.therapeutic_approaches = {
                'western_cbt': {
                    'description': 'Cognitive Behavioral Therapy',
                    'techniques': ['thought challenging', 'behavioral experiments', 'goal setting'],
                    'suitable_for': ['anxiety', 'depression', 'phobias'],
                    'cultural_fit': ['western', 'individualistic']
                },
                'eastern_mindfulness': {
                    'description': 'Mindfulness-based approaches',
                    'techniques': ['meditation', 'breathing exercises', 'present moment awareness'],
                    'suitable_for': ['stress', 'anxiety', 'emotional regulation'],
                    'cultural_fit': ['eastern', 'holistic']
                },
                'indigenous_healing': {
                    'description': 'Traditional healing practices',
                    'techniques': ['storytelling', 'ritual practices', 'connection with nature'],
                    'suitable_for': ['trauma', 'identity issues', 'spiritual distress'],
                    'cultural_fit': ['indigenous', 'traditional']
                },
                'family_systemic': {
                    'description': 'Family and community-based therapy',
                    'techniques': ['family involvement', 'community support', 'systemic approaches'],
                    'suitable_for': ['family conflicts', 'relationship issues', 'cultural transitions'],
                    'cultural_fit': ['collectivistic', 'family-oriented']
                }
            }
            
            logger.info("Cultural data loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load cultural data: {e}")
            raise CulturalAdaptationError(f"Cultural data loading failed: {e}", "CULT_001")
    
    async def get_context(self, user_profile: Dict[str, Any], language: str) -> Dict[str, Any]:
        """
        Get cultural context for a user
        
        Args:
            user_profile: User profile information
            language: Detected language
            
        Returns:
            Dict[str, Any]: Cultural context
        """
        try:
            # Determine cultural region from language and profile
            cultural_region = self._determine_cultural_region(language, user_profile)
            
            # Get cultural profile
            cultural_profile = self.metaphors_database.get(cultural_region, self.metaphors_database['western'])
            
            # Get appropriate therapeutic approach
            therapeutic_approach = self._select_therapeutic_approach(cultural_region, user_profile)
            
            context = {
                'cultural_region': cultural_region,
                'language': language,
                'communication_style': cultural_profile['communication_style'],
                'family_involvement': cultural_profile['family_involvement'],
                'spiritual_aspect': cultural_profile['spiritual_aspect'],
                'therapeutic_approach': therapeutic_approach,
                'metaphors': cultural_profile['therapy_concepts'],
                'user_preferences': user_profile.get('preferences', {})
            }
            
            logger.debug(f"Generated cultural context: {context}")
            return context
            
        except Exception as e:
            logger.error(f"Failed to get cultural context: {e}")
            raise CulturalAdaptationError(f"Cultural context generation failed: {e}", "CULT_001")
    
    def _determine_cultural_region(self, language: str, user_profile: Dict[str, Any]) -> str:
        """Determine cultural region based on language and profile"""
        # Language to region mapping
        language_regions = {
            'en': 'western',
            'es': 'latin',
            'fr': 'western',
            'de': 'western',
            'it': 'western',
            'pt': 'latin',
            'ru': 'eastern',
            'zh': 'eastern',
            'ja': 'eastern',
            'ko': 'eastern',
            'ar': 'eastern',
            'hi': 'eastern',
            'th': 'eastern',
            'vi': 'eastern',
            'sw': 'african',
            'am': 'african',
            'yo': 'african',
            'ig': 'african',
            'ha': 'african',
            'zu': 'african',
            'xh': 'african'
        }
        
        # Check user profile for cultural preferences
        if 'cultural_background' in user_profile:
            return user_profile['cultural_background']
        
        # Use language-based mapping
        return language_regions.get(language, 'western')
    
    def _select_therapeutic_approach(self, cultural_region: str, user_profile: Dict[str, Any]) -> str:
        """Select appropriate therapeutic approach"""
        region_approaches = {
            'western': 'western_cbt',
            'eastern': 'eastern_mindfulness',
            'african': 'indigenous_healing',
            'latin': 'family_systemic'
        }
        
        # Check user preferences
        if 'preferred_approach' in user_profile:
            return user_profile['preferred_approach']
        
        # Return region-based approach
        return region_approaches.get(cultural_region, 'western_cbt')
    
    async def adapt_response(self, response: str, cultural_context: Dict[str, Any]) -> str:
        """
        Adapt response based on cultural context
        
        Args:
            response: Original response
            cultural_context: Cultural context
            
        Returns:
            str: Culturally adapted response
        """
        try:
            cultural_region = cultural_context.get('cultural_region', 'western')
            communication_style = cultural_context.get('communication_style', 'direct')
            
            # Apply cultural adaptations
            adapted_response = response
            
            # Communication style adaptations
            if communication_style == 'indirect':
                adapted_response = self._make_indirect(adapted_response)
            elif communication_style == 'expressive':
                adapted_response = self._make_expressive(adapted_response)
            elif communication_style == 'narrative':
                adapted_response = self._make_narrative(adapted_response)
            
            # Add cultural metaphors if appropriate
            if cultural_region in self.metaphors_database:
                adapted_response = self._add_cultural_metaphors(adapted_response, cultural_region)
            
            return adapted_response
            
        except Exception as e:
            logger.error(f"Response adaptation failed: {e}")
            return response  # Return original if adaptation fails
    
    def _make_indirect(self, response: str) -> str:
        """Make response more indirect for Eastern cultures"""
        # Add gentle qualifiers
        qualifiers = ['Perhaps', 'It might be that', 'One possibility is', 'You might consider']
        if not any(q in response for q in qualifiers):
            response = f"Perhaps {response.lower()}"
        
        # Soften direct statements
        response = response.replace("You should", "You might consider")
        response = response.replace("You need to", "It may be helpful to")
        response = response.replace("You must", "It might be wise to")
        
        return response
    
    def _make_expressive(self, response: str) -> str:
        """Make response more expressive for Latin cultures"""
        # Add emotional warmth
        if not response.endswith('.'):
            response += '.'
        
        # Add culturally appropriate expressions
        expressions = [
            'Con cariño (with care)',
            'You have fortaleza (strength)',
            'La familia is important',
            'Tu corazón (your heart) knows'
        ]
        
        # Randomly add an expression (10% chance)
        if random.random() < 0.1:
            response += f" {random.choice(expressions)}."
        
        return response
    
    def _make_narrative(self, response: str) -> str:
        """Make response more narrative for African cultures"""
        # Add storytelling elements
        narrative_starters = [
            'In many traditions, ',
            'Our ancestors understood that ',
            'The wisdom of generations teaches us that ',
            'Stories from our communities remind us that '
        ]
        
        # Add narrative element (20% chance)
        if random.random() < 0.2 and not any(starter in response for starter in narrative_starters):
            response = f"{random.choice(narrative_starters)}{response.lower()}"
        
        return response
    
    def _add_cultural_metaphors(self, response: str, cultural_region: str) -> str:
        """Add appropriate cultural metaphors"""
        try:
            cultural_data = self.metaphors_database.get(cultural_region, {})
            therapy_concepts = cultural_data.get('therapy_concepts', {})
            
            # Replace generic terms with culturally appropriate ones
            for concept, alternatives in therapy_concepts.items():
                if concept in response.lower():
                    # Replace with culturally appropriate alternative
                    replacement = random.choice(alternatives)
                    response = response.replace(concept, replacement)
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to add cultural metaphors: {e}")
            return response
    
    async def initialize(self):
        """Initialize cultural adapter"""
        try:
            logger.info("Cultural adapter initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Cultural adapter initialization failed: {e}")
            return False
    
    def _add_spiritual_elements(self, response: str, cultural_region: str) -> str:
        """Add spiritual elements based on cultural region"""
        spiritual_phrases = {
            'eastern': [
                "finding balance within yourself",
                "connecting with your inner wisdom",
                "cultivating inner peace"
            ],
            'african': [
                "drawing strength from your ancestors",
                "finding wholeness in community",
                "healing through connection"
            ],
            'latin': [
                "finding strength in faith",
                "drawing on family support",
                "trusting in divine guidance"
            ]
        }
        
        phrases = spiritual_phrases.get(cultural_region, [])
        if phrases:
            response += f" Remember, {phrases[0]} can provide additional support."
        
        return response
    
    async def get_emergency_resources(self, cultural_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get culturally appropriate emergency resources
        
        Args:
            cultural_context: Cultural context
            
        Returns:
            List[Dict[str, Any]]: Emergency resources
        """
        try:
            cultural_region = cultural_context.get('cultural_region', 'western')
            language = cultural_context.get('language', 'en')
            
            # Base emergency resources
            resources = [
                {
                    'type': 'crisis_hotline',
                    'name': 'National Crisis Hotline',
                    'phone': '988',
                    'available_24_7': True,
                    'languages': ['en']
                }
            ]
            
            # Add culturally specific resources
            if cultural_region == 'african':
                resources.append({
                    'type': 'community_elder',
                    'name': 'Community Elder Support',
                    'description': 'Connect with community elders for guidance',
                    'cultural_relevance': 'high'
                })
            elif cultural_region == 'latin':
                resources.append({
                    'type': 'family_support',
                    'name': 'Family Support Network',
                    'description': 'Engage family members for support',
                    'cultural_relevance': 'high'
                })
            elif cultural_region == 'eastern':
                resources.append({
                    'type': 'spiritual_guidance',
                    'name': 'Spiritual Guidance',
                    'description': 'Connect with spiritual advisors',
                    'cultural_relevance': 'high'
                })
            
            return resources
            
        except Exception as e:
            logger.error(f"Failed to get emergency resources: {e}")
            raise CulturalAdaptationError(f"Emergency resources failed: {e}", "CULT_001")
    
    
    def get_cultural_statistics(self) -> Dict[str, Any]:
        """Get cultural adaptation statistics"""
        return {
            'supported_regions': len(self.metaphors_database),
            'therapeutic_approaches': len(self.therapeutic_approaches),
            'cultural_frameworks': len(self.cultural_frameworks)
        }

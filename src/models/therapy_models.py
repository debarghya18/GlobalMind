"""
Therapy AI models for GlobalMind
Implements evidence-based therapeutic approaches
"""

import asyncio
from typing import Dict, Any, List, Optional
from loguru import logger
import random
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer
import numpy as np

from ..core.config import ModelsConfig
from ..core.exceptions import ModelError


class TherapyModels:
    """AI models for therapeutic conversations"""
    
    def __init__(self, config: ModelsConfig):
        """
        Initialize therapy models
        
        Args:
            config: Models configuration
        """
        self.config = config
        self.models = {}
        self.therapeutic_frameworks = {
            'western_cbt': self._load_cbt_responses(),
            'eastern_mindfulness': self._load_mindfulness_responses(),
            'indigenous_healing': self._load_indigenous_responses(),
            'family_systemic': self._load_family_responses(),
            'religious_spiritual': self._load_spiritual_responses(),
            'narrative_therapy': self._load_narrative_responses()
        }
        
        logger.info("Therapy models initialized")
    
    def _load_cbt_responses(self) -> Dict[str, List[str]]:
        """Load CBT (Cognitive Behavioral Therapy) responses"""
        return {
            'greeting': [
                "Hello! I'm here to support you today. What's on your mind?",
                "Welcome! How are you feeling right now?",
                "Hi there! I'm glad you're here. What would you like to talk about?",
                "Good to see you! What's been happening in your life lately?"
            ],
            'anxiety': [
                "I understand you're feeling anxious. Let's try to identify what thoughts might be contributing to this feeling.",
                "Anxiety can feel overwhelming. Can you tell me what specific thoughts are going through your mind right now?",
                "It's completely normal to feel anxious sometimes. Let's work together to examine these worried thoughts.",
                "When you notice anxiety, try the 4-7-8 breathing technique: breathe in for 4, hold for 7, exhale for 8."
            ],
            'depression': [
                "I hear that you're struggling with difficult feelings. Depression can make everything feel harder.",
                "These feelings are valid, and you're not alone. What small step could we take together today?",
                "Depression often involves negative thought patterns. Let's examine some of these thoughts together.",
                "Even small activities can help when feeling depressed. What's one thing you enjoyed doing in the past?"
            ],
            'negative_thoughts': [
                "Let's examine this thought. What evidence supports it, and what evidence challenges it?",
                "Is this thought helpful to you right now? How might you reframe it more positively?",
                "What would you tell a friend who had this same thought?",
                "Let's try the thought record technique. Rate how much you believe this thought from 1-10."
            ],
            'coping_strategies': [
                "One effective strategy is the 5-4-3-2-1 grounding technique. Can you name 5 things you can see right now?",
                "Progressive muscle relaxation can help. Try tensing and releasing each muscle group.",
                "Journaling can help process difficult emotions. What thoughts would you like to write down?",
                "Physical activity, even a short walk, can significantly improve mood. Is this something you could try?"
            ],
            'encouragement': [
                "You're showing real strength by reaching out for support.",
                "Remember, healing is a process, and you're taking important steps.",
                "Every small step forward is progress worth celebrating.",
                "You have more resilience than you might realize right now."
            ]
        }
    
    def _load_mindfulness_responses(self) -> Dict[str, List[str]]:
        """Load mindfulness-based responses"""
        return {
            'greeting': [
                "Welcome. Take a moment to breathe and notice how you're feeling in this present moment.",
                "Hello. Let's begin by taking three deep breaths together.",
                "Greetings. I invite you to settle into this moment with gentle awareness.",
                "Welcome to this space of mindful presence. What brings you here today?"
            ],
            'anxiety': [
                "Notice where you feel the anxiety in your body. Can you breathe into that space with compassion?",
                "Anxiety is a visitor, not a permanent resident. Let's observe it with curiosity rather than judgment.",
                "When anxiety arises, return to your breath as an anchor in the present moment.",
                "Place one hand on your heart and one on your belly. Feel the natural rhythm of your breathing."
            ],
            'depression': [
                "Depression can feel like a heavy cloud. Can we sit with this feeling without trying to change it?",
                "Notice any judgments about your depression. Can we meet these feelings with kindness instead?",
                "What does your body need right now? Sometimes gentle movement or rest can be healing.",
                "Even in difficult moments, your breath continues to sustain you. This too shall pass."
            ],
            'mindfulness_practices': [
                "Let's try a body scan. Starting with your toes, notice any sensations without trying to change them.",
                "Focus on your breath. When your mind wanders, gently guide your attention back without judgment.",
                "Listen to the sounds around you for one minute. Notice how they arise and fade away.",
                "Observe your thoughts like clouds passing in the sky - acknowledge them and let them go."
            ],
            'acceptance': [
                "What you're experiencing right now is part of the human experience. You're not alone.",
                "Can we practice accepting this moment exactly as it is, without needing it to be different?",
                "Resistance often increases suffering. What would it feel like to soften around this experience?",
                "Your feelings are valid messengers. What might they be trying to tell you?"
            ]
        }
    
    def _load_indigenous_responses(self) -> Dict[str, List[str]]:
        """Load indigenous healing responses"""
        return {
            'greeting': [
                "Welcome, friend. Our ancestors remind us that healing happens in community and connection.",
                "I honor your presence here. In many traditions, sharing our burdens lightens them.",
                "Greetings. Like the circle of seasons, our healing journey has its own natural rhythm.",
                "Welcome to this sacred space of sharing and healing."
            ],
            'connection': [
                "In many traditions, we understand that our wellness is connected to our relationships and community.",
                "Your ancestors carried wisdom that lives within you. What guidance might they offer now?",
                "The earth beneath us and sky above us remind us we are part of something larger.",
                "Stories have always been medicine. What story is your heart wanting to tell?"
            ],
            'nature_healing': [
                "Nature offers us powerful medicine. When did you last feel connected to the natural world?",
                "The cycles of nature remind us that after every winter comes spring. Your healing has its own season.",
                "Water cleanses, earth grounds, fire transforms, air renews. Which element calls to you today?",
                "Our ancestors knew that walking on the earth could heal both body and spirit."
            ],
            'community': [
                "Healing often happens in relationship with others. Who are your sources of support?",
                "In community, we can carry each other's burdens. You don't have to face this alone.",
                "Your struggles affect not just you, but ripple through your connections. Healing benefits all.",
                "What gifts do you have to offer your community, even in your time of struggle?"
            ]
        }
    
    def _load_family_responses(self) -> Dict[str, List[str]]:
        """Load family systemic responses"""
        return {
            'greeting': [
                "Welcome! I'm interested in understanding not just your experience, but your important relationships too.",
                "Hello! Family and close relationships often play a big role in how we feel. Tell me about yours.",
                "Greetings! We are all shaped by our connections with others. What brings you here today?",
                "Welcome to this space where we can explore how your relationships support your wellbeing."
            ],
            'family_dynamics': [
                "How do you think your family members would describe what you're going through?",
                "What patterns do you notice in your family when someone is struggling?",
                "Who in your family or close circle has been most supportive during difficult times?",
                "Sometimes our struggles reflect larger family patterns. What do you notice about this?"
            ],
            'support_systems': [
                "Let's map out your support network. Who are the people you can truly count on?",
                "How does your family typically handle stress or difficult emotions?",
                "What role do you usually play in your family during challenging times?",
                "How might involving your support system help with what you're experiencing?"
            ],
            'cultural_family': [
                "What cultural values about family and community did you grow up with?",
                "How do your cultural background and family traditions influence your healing process?",
                "What wisdom has been passed down in your family about handling life's challenges?",
                "How might your family's cultural practices support your wellbeing right now?"
            ]
        }
    
    def _load_spiritual_responses(self) -> Dict[str, List[str]]:
        """Load spiritual/religious responses"""
        return {
            'greeting': [
                "Peace be with you. I honor the sacred within you as we begin this conversation.",
                "Blessings to you. Many find strength in their spiritual beliefs during difficult times.",
                "Welcome. Your spirit, however you understand it, is an important part of your healing.",
                "Greetings, friend. What role does your spiritual life play in your current experience?"
            ],
            'faith_strength': [
                "How has your faith or spiritual practice been a source of strength for you?",
                "What spiritual practices bring you comfort during difficult times?",
                "Many traditions speak of finding meaning in suffering. How does this resonate with you?",
                "Prayer, meditation, or spiritual reflection can be powerful healing tools. What works for you?"
            ],
            'meaning_purpose': [
                "How do you understand your current struggles in the context of your life's purpose?",
                "What gives your life meaning, especially during challenging times?",
                "Many spiritual traditions speak of growth through adversity. How might this apply to you?",
                "What would your spiritual tradition say about finding hope in difficult circumstances?"
            ],
            'community_worship': [
                "How has your spiritual community supported you during this time?",
                "What role do spiritual rituals or practices play in your healing?",
                "Many find strength in communal worship or spiritual fellowship. Is this true for you?",
                "How might your spiritual beliefs guide you in taking care of yourself right now?"
            ]
        }
    
    def _load_narrative_responses(self) -> Dict[str, List[str]]:
        """Load narrative therapy responses"""
        return {
            'greeting': [
                "Welcome! I'm interested in hearing your story and the unique experiences that shape who you are.",
                "Hello! Every person has a rich story. I'd love to learn more about yours.",
                "Greetings! You are the expert on your own life. What part of your story would you like to share?",
                "Welcome to this space where your story matters and your voice is heard."
            ],
            'story_exploration': [
                "Tell me more about how this problem has affected your life story.",
                "What chapter of your life feels most relevant to what you're experiencing now?",
                "How would you like your story to continue from this point?",
                "What strengths and resources from your past might help you with this current challenge?"
            ],
            'externalizing': [
                "It sounds like depression has been telling you some harsh stories about yourself. Is that accurate?",
                "How long has anxiety been interfering with the life you want to live?",
                "What would you like to say back to the voice of self-doubt?",
                "When hasn't this problem had such a strong influence over your life?"
            ],
            'unique_outcomes': [
                "Tell me about a time when you didn't let this problem control your actions.",
                "What does it say about you as a person that you're here seeking support?",
                "When have you surprised yourself with your own strength or resilience?",
                "What would people who know you well say are your most important qualities?"
            ]
        }
    
    async def load_models(self):
        """Load AI models (placeholder for actual model loading)"""
        try:
            # In a real implementation, this would load actual AI models
            # For now, we'll simulate model loading
            logger.info("Loading therapy models...")
            
            # Simulate loading time
            await asyncio.sleep(1)
            
            self.models['loaded'] = True
            logger.info("Therapy models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load therapy models: {e}")
            raise ModelError(f"Model loading failed: {e}", "MODEL_001")
    
    async def generate_response(
        self, 
        user_input: str, 
        cultural_context: Dict[str, Any], 
        session_history: List[Dict[str, Any]] = None
    ) -> str:
        """
        Generate therapeutic response based on cultural context
        
        Args:
            user_input: User's message
            cultural_context: Cultural adaptation context
            session_history: Previous conversation history
            
        Returns:
            str: Generated therapeutic response
        """
        try:
            # Get therapeutic approach from cultural context
            therapeutic_approach = cultural_context.get('therapeutic_approach', 'western_cbt')
            
            # Analyze user input for key themes
            themes = self._analyze_input_themes(user_input.lower())
            
            # Select appropriate response framework
            framework = self.therapeutic_frameworks.get(therapeutic_approach, self.therapeutic_frameworks['western_cbt'])
            
            # Generate contextual response
            response = self._generate_contextual_response(themes, framework, cultural_context)
            
            # Add cultural adaptation
            from ..cultural.adapter import CulturalAdapter
            cultural_adapter = CulturalAdapter([], {})
            adapted_response = await cultural_adapter.adapt_response(response, cultural_context)
            
            logger.debug(f"Generated response using {therapeutic_approach} approach")
            return adapted_response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "I'm here to listen and support you. Can you tell me more about what you're experiencing?"
    
    def _analyze_input_themes(self, user_input: str) -> List[str]:
        """Analyze user input for therapeutic themes"""
        themes = []
        
        # Anxiety indicators
        anxiety_words = ['anxious', 'worried', 'nervous', 'panic', 'stress', 'overwhelmed', 'fear']
        if any(word in user_input for word in anxiety_words):
            themes.append('anxiety')
        
        # Depression indicators
        depression_words = ['sad', 'depressed', 'hopeless', 'empty', 'worthless', 'tired', 'lonely']
        if any(word in user_input for word in depression_words):
            themes.append('depression')
        
        # Negative thinking patterns
        negative_words = ['always', 'never', 'terrible', 'awful', 'disaster', 'failure', 'stupid']
        if any(word in user_input for word in negative_words):
            themes.append('negative_thoughts')
        
        # Greeting/initial contact
        greeting_words = ['hello', 'hi', 'hey', 'good morning', 'good day']
        if any(word in user_input for word in greeting_words):
            themes.append('greeting')
        
        # If no specific themes detected, use general support
        if not themes:
            themes.append('general_support')
        
        return themes
    
    def _generate_contextual_response(
        self, 
        themes: List[str], 
        framework: Dict[str, List[str]], 
        cultural_context: Dict[str, Any]
    ) -> str:
        """Generate response based on themes and framework"""
        
        # Priority order for theme selection
        theme_priority = ['greeting', 'anxiety', 'depression', 'negative_thoughts']
        
        # Select highest priority theme
        selected_theme = 'general_support'
        for theme in theme_priority:
            if theme in themes:
                selected_theme = theme
                break
        
        # Get responses for the theme
        if selected_theme in framework:
            responses = framework[selected_theme]
        else:
            # Fallback to encouragement or general responses
            responses = framework.get('encouragement', [
                "I'm here to support you through this.",
                "Thank you for sharing with me. Your feelings are valid.",
                "You're taking an important step by reaching out.",
                "Let's work through this together, one step at a time."
            ])
        
        # Select a response (could be made more sophisticated)
        response = random.choice(responses)
        
        return response
    
    async def generate_crisis_response(
        self, 
        user_input: str, 
        cultural_context: Dict[str, Any]
    ) -> str:
        """
        Generate crisis-specific response
        
        Args:
            user_input: User's message indicating crisis
            cultural_context: Cultural context
            
        Returns:
            str: Crisis-appropriate response
        """
        try:
            cultural_region = cultural_context.get('cultural_region', 'western')
            
            crisis_responses = {
                'western': [
                    "I'm really concerned about you right now. You're not alone, and there are people who want to help.",
                    "What you're feeling is overwhelming, but these feelings can change. Let's get you some immediate support.",
                    "I hear that you're in a lot of pain right now. There are crisis counselors available 24/7 who specialize in helping.",
                    "You've reached out, which shows incredible strength. Let's connect you with immediate professional support."
                ],
                'eastern': [
                    "I understand you're experiencing great suffering. In times of crisis, it's important to remember you're part of a larger whole.",
                    "Your life has value and meaning, even in this moment of darkness. Let's find you immediate support.",
                    "This moment of intense pain can pass, like clouds across the sky. There are people trained to help you right now.",
                    "You've shown wisdom by reaching out. Let's connect you with crisis support that understands your background."
                ],
                'african': [
                    "Our ancestors teach us that no one should face their darkest hour alone. There is immediate help available.",
                    "Your community values your life. Let's get you connected with crisis support right away.",
                    "In our tradition, reaching out for help is a sign of wisdom, not weakness. There are people ready to support you now.",
                    "Your story is not finished. There are crisis counselors who understand and want to help immediately."
                ],
                'latin': [
                    "Tu vida tiene valor. Your life has value. There are people who want to help you through this crisis immediately.",
                    "La familia and community want to support you. Let's get you connected with crisis help right now.",
                    "You have shown courage by reaching out. There is immediate help available from people who understand.",
                    "Esta crisis puede pasar. This crisis can pass. Let's get you professional support immediately."
                ]
            }
            
            responses = crisis_responses.get(cultural_region, crisis_responses['western'])
            response = random.choice(responses)
            
            # Add immediate action instructions
            response += "\n\n🆘 IMMEDIATE HELP:\n"
            response += "• Call 988 (US Crisis Lifeline)\n"
            response += "• Text 'HELLO' to 741741 (Crisis Text Line)\n"
            response += "• Go to your nearest emergency room\n"
            response += "• Call 911 if you're in immediate danger"
            
            return response
            
        except Exception as e:
            logger.error(f"Crisis response generation failed: {e}")
            return ("I'm very concerned about you. Please reach out for immediate help:\n"
                   "• Call 988 (Crisis Lifeline)\n"
                   "• Text 'HELLO' to 741741\n"
                   "• Go to your nearest emergency room\n"
                   "• Call 911 if in immediate danger")
    
    async def health_check(self) -> bool:
        """
        Perform health check on therapy models
        
        Returns:
            bool: True if healthy
        """
        try:
            # Test response generation
            test_response = await self.generate_response(
                "Hello, I'm feeling anxious",
                {'therapeutic_approach': 'western_cbt', 'cultural_region': 'western'}
            )
            
            return bool(test_response and len(test_response) > 10)
            
        except Exception as e:
            logger.error(f"Therapy models health check failed: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup model resources"""
        try:
            # Clear loaded models
            self.models.clear()
            logger.info("Therapy models cleanup completed")
            
        except Exception as e:
            logger.error(f"Therapy models cleanup failed: {e}")
    
    def get_supported_approaches(self) -> List[str]:
        """Get list of supported therapeutic approaches"""
        return list(self.therapeutic_frameworks.keys())
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Get model statistics"""
        return {
            'therapeutic_frameworks': len(self.therapeutic_frameworks),
            'total_responses': sum(
                len(responses) for framework in self.therapeutic_frameworks.values()
                for responses in framework.values()
            ),
            'models_loaded': self.models.get('loaded', False)
        }

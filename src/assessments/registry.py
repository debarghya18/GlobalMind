"""
Assessment Registry - Maps user-friendly names to technical assessments
Provides transparent access to psychological assessments with patient-friendly names
"""

from typing import Dict, List, Optional, Type, Set
from enum import Enum
from dataclasses import dataclass, field

from .base import PsychologicalAssessment, AssessmentType


class AssessmentCategory(Enum):
    """Categories of assessments for organization"""
    MOOD = "mood"
    ANXIETY = "anxiety"
    ATTENTION = "attention"
    TRAUMA = "trauma"
    PERSONALITY = "personality"
    SUBSTANCE_USE = "substance_use"
    EATING = "eating"
    GENERAL_WELLBEING = "general_wellbeing"
    SPECIALIZED = "specialized"


@dataclass
class AssessmentInfo:
    """Information about an assessment for the registry"""
    technical_name: str
    user_friendly_name: str
    description: str
    category: AssessmentCategory
    assessment_type: AssessmentType
    estimated_time_minutes: int
    target_age_range: str = "18+"
    requires_supervision: bool = False
    cultural_adaptations_available: List[str] = field(default_factory=list)
    languages_available: List[str] = field(default_factory=lambda: ["English"])
    tags: Set[str] = field(default_factory=set)
    is_screening: bool = True  # vs diagnostic tool
    is_self_report: bool = True  # vs clinician-administered
    normative_data_available: bool = False
    
    def __post_init__(self):
        # Ensure tags is a set
        if isinstance(self.tags, list):
            self.tags = set(self.tags)


class AssessmentRegistry:
    """Registry for managing psychological assessments with user-friendly names"""
    
    def __init__(self):
        self._assessments: Dict[str, AssessmentInfo] = {}
        self._user_friendly_to_technical: Dict[str, str] = {}
        self._technical_to_user_friendly: Dict[str, str] = {}
        self._assessment_classes: Dict[str, Type[PsychologicalAssessment]] = {}
        self._register_default_assessments()
    
    def _register_default_assessments(self):
        """Register all default assessments with their user-friendly names"""
        
        # Depression Assessments
        self.register_assessment(AssessmentInfo(
            technical_name="PHQ-9",
            user_friendly_name="Wellness Check",
            description="A brief questionnaire to assess your overall wellness and mood patterns over the past two weeks.",
            category=AssessmentCategory.MOOD,
            assessment_type=AssessmentType.DEPRESSION,
            estimated_time_minutes=3,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian", "African American"],
            languages_available=["English", "Spanish", "French", "German"],
            tags={"depression", "mood", "screening", "primary_care"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        self.register_assessment(AssessmentInfo(
            technical_name="Beck Depression Inventory-II",
            user_friendly_name="Mood Assessment",
            description="A comprehensive evaluation of your mood and emotional well-being to help identify areas for support.",
            category=AssessmentCategory.MOOD,
            assessment_type=AssessmentType.DEPRESSION,
            estimated_time_minutes=10,
            target_age_range="13+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian"],
            languages_available=["English", "Spanish"],
            tags={"depression", "mood", "comprehensive", "validated"},
            is_screening=False,
            is_self_report=True,
            normative_data_available=True
        ))
        
        self.register_assessment(AssessmentInfo(
            technical_name="Hamilton Depression Rating Scale",
            user_friendly_name="Daily Life Evaluation",
            description="An assessment of how your daily activities and routines have been affected by your mood.",
            category=AssessmentCategory.MOOD,
            assessment_type=AssessmentType.DEPRESSION,
            estimated_time_minutes=15,
            target_age_range="18+",
            requires_supervision=True,
            cultural_adaptations_available=["Hispanic"],
            languages_available=["English", "Spanish"],
            tags={"depression", "daily_functioning", "clinician_administered"},
            is_screening=False,
            is_self_report=False,
            normative_data_available=True
        ))
        
        # Anxiety Assessments
        self.register_assessment(AssessmentInfo(
            technical_name="GAD-7",
            user_friendly_name="Stress Level Check",
            description="A quick assessment to understand your stress levels and how they might be affecting your daily life.",
            category=AssessmentCategory.ANXIETY,
            assessment_type=AssessmentType.ANXIETY,
            estimated_time_minutes=3,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian", "African American"],
            languages_available=["English", "Spanish", "French", "German", "Chinese"],
            tags={"anxiety", "stress", "screening", "primary_care"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        self.register_assessment(AssessmentInfo(
            technical_name="Beck Anxiety Inventory",
            user_friendly_name="Worry Assessment",
            description="A detailed evaluation of worry patterns and physical symptoms to help understand your anxiety.",
            category=AssessmentCategory.ANXIETY,
            assessment_type=AssessmentType.ANXIETY,
            estimated_time_minutes=8,
            target_age_range="17+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian"],
            languages_available=["English", "Spanish"],
            tags={"anxiety", "worry", "physical_symptoms", "validated"},
            is_screening=False,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # ADHD Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="ADHD Self-Report Scale",
            user_friendly_name="Focus & Attention Check",
            description="An assessment of your attention patterns and focus abilities in daily activities.",
            category=AssessmentCategory.ATTENTION,
            assessment_type=AssessmentType.ADHD,
            estimated_time_minutes=10,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian"],
            languages_available=["English", "Spanish"],
            tags={"adhd", "attention", "focus", "concentration"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # OCD Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="Yale-Brown Obsessive Compulsive Scale",
            user_friendly_name="Thought Patterns Assessment",
            description="An evaluation of repetitive thoughts and behaviors to better understand your mental patterns.",
            category=AssessmentCategory.SPECIALIZED,
            assessment_type=AssessmentType.OCD,
            estimated_time_minutes=20,
            target_age_range="18+",
            requires_supervision=True,
            cultural_adaptations_available=["Hispanic"],
            languages_available=["English", "Spanish"],
            tags={"ocd", "obsessions", "compulsions", "repetitive_thoughts"},
            is_screening=False,
            is_self_report=False,
            normative_data_available=True
        ))
        
        # PTSD Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="PCL-5",
            user_friendly_name="Life Experiences Check",
            description="A questionnaire about challenging life experiences and how they might be affecting you now.",
            category=AssessmentCategory.TRAUMA,
            assessment_type=AssessmentType.PTSD,
            estimated_time_minutes=10,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian", "African American", "Native American"],
            languages_available=["English", "Spanish", "French"],
            tags={"ptsd", "trauma", "life_experiences", "symptoms"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # Bipolar Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="Mood Disorder Questionnaire",
            user_friendly_name="Energy & Mood Check",
            description="An assessment of your energy levels and mood changes to understand your emotional patterns.",
            category=AssessmentCategory.MOOD,
            assessment_type=AssessmentType.BIPOLAR,
            estimated_time_minutes=5,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian"],
            languages_available=["English", "Spanish"],
            tags={"bipolar", "mood_swings", "energy", "screening"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # General Health Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="SF-36",
            user_friendly_name="Life Quality Check",
            description="A comprehensive assessment of your overall quality of life and well-being across different areas.",
            category=AssessmentCategory.GENERAL_WELLBEING,
            assessment_type=AssessmentType.GENERAL,
            estimated_time_minutes=15,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian", "African American"],
            languages_available=["English", "Spanish", "French", "German", "Chinese"],
            tags={"quality_of_life", "general_health", "wellbeing", "comprehensive"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # Personality Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="Big Five Inventory",
            user_friendly_name="Personality Insights",
            description="An exploration of your personality traits and how they influence your interactions and preferences.",
            category=AssessmentCategory.PERSONALITY,
            assessment_type=AssessmentType.PERSONALITY,
            estimated_time_minutes=15,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian", "African American"],
            languages_available=["English", "Spanish", "French", "German"],
            tags={"personality", "traits", "self_understanding", "insights"},
            is_screening=False,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # Substance Use Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="AUDIT",
            user_friendly_name="Lifestyle Habits Check",
            description="A confidential assessment of your lifestyle habits and their impact on your well-being.",
            category=AssessmentCategory.SUBSTANCE_USE,
            assessment_type=AssessmentType.SUBSTANCE,
            estimated_time_minutes=5,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian", "African American"],
            languages_available=["English", "Spanish", "French"],
            tags={"substance_use", "lifestyle", "habits", "screening"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
        
        # Eating Disorder Assessment
        self.register_assessment(AssessmentInfo(
            technical_name="EAT-26",
            user_friendly_name="Nutrition & Wellness Check",
            description="An assessment of your relationship with food and eating patterns to support your overall wellness.",
            category=AssessmentCategory.EATING,
            assessment_type=AssessmentType.EATING,
            estimated_time_minutes=8,
            target_age_range="18+",
            requires_supervision=False,
            cultural_adaptations_available=["Hispanic", "Asian"],
            languages_available=["English", "Spanish"],
            tags={"eating_disorders", "nutrition", "body_image", "wellness"},
            is_screening=True,
            is_self_report=True,
            normative_data_available=True
        ))
    
    def register_assessment(self, assessment_info: AssessmentInfo):
        """Register an assessment in the registry"""
        self._assessments[assessment_info.technical_name] = assessment_info
        self._user_friendly_to_technical[assessment_info.user_friendly_name] = assessment_info.technical_name
        self._technical_to_user_friendly[assessment_info.technical_name] = assessment_info.user_friendly_name
    
    def register_assessment_class(self, technical_name: str, assessment_class: Type[PsychologicalAssessment]):
        """Register an assessment class implementation"""
        self._assessment_classes[technical_name] = assessment_class
    
    def get_assessment_info(self, identifier: str) -> Optional[AssessmentInfo]:
        """Get assessment info by technical name or user-friendly name"""
        # Try technical name first
        if identifier in self._assessments:
            return self._assessments[identifier]
        
        # Try user-friendly name
        technical_name = self._user_friendly_to_technical.get(identifier)
        if technical_name:
            return self._assessments[technical_name]
        
        return None
    
    def get_user_friendly_name(self, technical_name: str) -> Optional[str]:
        """Get user-friendly name from technical name"""
        return self._technical_to_user_friendly.get(technical_name)
    
    def get_technical_name(self, user_friendly_name: str) -> Optional[str]:
        """Get technical name from user-friendly name"""
        return self._user_friendly_to_technical.get(user_friendly_name)
    
    def create_assessment(self, identifier: str, cultural_context: Optional[str] = None) -> Optional[PsychologicalAssessment]:
        """Create an assessment instance by identifier (technical or user-friendly name)"""
        # Get technical name
        technical_name = identifier
        if identifier in self._user_friendly_to_technical:
            technical_name = self._user_friendly_to_technical[identifier]
        
        # Get assessment class
        assessment_class = self._assessment_classes.get(technical_name)
        if not assessment_class:
            return None
        
        # Create instance
        return assessment_class(cultural_context=cultural_context)
    
    def list_assessments(self, 
                        category: Optional[AssessmentCategory] = None,
                        assessment_type: Optional[AssessmentType] = None,
                        user_friendly_names_only: bool = True) -> List[str]:
        """List available assessments, optionally filtered by category or type"""
        assessments = []
        
        for info in self._assessments.values():
            # Apply filters
            if category and info.category != category:
                continue
            if assessment_type and info.assessment_type != assessment_type:
                continue
            
            # Choose name format
            if user_friendly_names_only:
                assessments.append(info.user_friendly_name)
            else:
                assessments.append(f"{info.user_friendly_name} ({info.technical_name})")
        
        return sorted(assessments)
    
    def search_assessments(self, query: str, user_friendly_names_only: bool = True) -> List[str]:
        """Search assessments by name, description, or tags"""
        query = query.lower()
        results = []
        
        for info in self._assessments.values():
            # Search in names
            if (query in info.user_friendly_name.lower() or 
                query in info.technical_name.lower() or
                query in info.description.lower()):
                
                if user_friendly_names_only:
                    results.append(info.user_friendly_name)
                else:
                    results.append(f"{info.user_friendly_name} ({info.technical_name})")
                continue
            
            # Search in tags
            if any(query in tag.lower() for tag in info.tags):
                if user_friendly_names_only:
                    results.append(info.user_friendly_name)
                else:
                    results.append(f"{info.user_friendly_name} ({info.technical_name})")
        
        return sorted(results)
    
    def get_assessments_by_category(self, category: AssessmentCategory) -> List[AssessmentInfo]:
        """Get all assessments in a specific category"""
        return [info for info in self._assessments.values() if info.category == category]
    
    def get_assessments_by_type(self, assessment_type: AssessmentType) -> List[AssessmentInfo]:
        """Get all assessments of a specific type"""
        return [info for info in self._assessments.values() if info.assessment_type == assessment_type]
    
    def get_screening_assessments(self) -> List[AssessmentInfo]:
        """Get all screening assessments"""
        return [info for info in self._assessments.values() if info.is_screening]
    
    def get_self_report_assessments(self) -> List[AssessmentInfo]:
        """Get all self-report assessments"""
        return [info for info in self._assessments.values() if info.is_self_report]
    
    def get_assessments_for_culture(self, culture: str) -> List[AssessmentInfo]:
        """Get assessments that have cultural adaptations for a specific culture"""
        return [info for info in self._assessments.values() 
                if culture in info.cultural_adaptations_available]
    
    def get_assessments_for_language(self, language: str) -> List[AssessmentInfo]:
        """Get assessments available in a specific language"""
        return [info for info in self._assessments.values() 
                if language in info.languages_available]
    
    def get_quick_assessments(self, max_time_minutes: int = 5) -> List[AssessmentInfo]:
        """Get quick assessments that take less than specified time"""
        return [info for info in self._assessments.values() 
                if info.estimated_time_minutes <= max_time_minutes]
    
    def get_assessment_suggestions(self, 
                                 presenting_concerns: List[str],
                                 cultural_context: Optional[str] = None,
                                 language: str = "English",
                                 max_time_minutes: Optional[int] = None) -> List[AssessmentInfo]:
        """Get assessment suggestions based on presenting concerns"""
        suggestions = []
        
        # Convert concerns to lowercase for matching
        concerns_lower = [concern.lower() for concern in presenting_concerns]
        
        for info in self._assessments.values():
            # Check if assessment matches concerns
            matches = False
            for concern in concerns_lower:
                if (concern in info.description.lower() or
                    any(concern in tag.lower() for tag in info.tags)):
                    matches = True
                    break
            
            if not matches:
                continue
            
            # Apply filters
            if cultural_context and cultural_context not in info.cultural_adaptations_available:
                continue
            
            if language not in info.languages_available:
                continue
            
            if max_time_minutes and info.estimated_time_minutes > max_time_minutes:
                continue
            
            suggestions.append(info)
        
        # Sort by relevance (screening tests first, then by estimated time)
        suggestions.sort(key=lambda x: (not x.is_screening, x.estimated_time_minutes))
        
        return suggestions
    
    def get_summary_statistics(self) -> Dict[str, int]:
        """Get summary statistics about the assessment registry"""
        stats = {
            'total_assessments': len(self._assessments),
            'screening_assessments': len(self.get_screening_assessments()),
            'self_report_assessments': len(self.get_self_report_assessments()),
            'culturally_adapted_assessments': len([info for info in self._assessments.values() 
                                                 if info.cultural_adaptations_available]),
            'multilingual_assessments': len([info for info in self._assessments.values() 
                                           if len(info.languages_available) > 1])
        }
        
        # Category breakdown
        for category in AssessmentCategory:
            stats[f'{category.value}_assessments'] = len(self.get_assessments_by_category(category))
        
        return stats


# Global registry instance
assessment_registry = AssessmentRegistry()

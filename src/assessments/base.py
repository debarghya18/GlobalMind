"""
Base classes for psychological assessments in GlobalMind
Uses user-friendly names to make assessments less intimidating
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from enum import Enum
import json

from loguru import logger


class AssessmentType(Enum):
    """Types of psychological assessments"""
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    ADHD = "adhd"
    OCD = "ocd"
    PTSD = "ptsd"
    BIPOLAR = "bipolar"
    GENERAL = "general"
    PERSONALITY = "personality"
    SUBSTANCE = "substance"
    EATING = "eating"


class SeverityLevel(Enum):
    """Severity levels for assessment results - user-friendly names"""
    MINIMAL = "minimal"
    MILD = "mild"
    MODERATE = "moderate"
    MODERATELY_SEVERE = "moderately_severe"
    SEVERE = "severe"
    VERY_SEVERE = "very_severe"
    
    @property
    def user_friendly_name(self) -> str:
        """Get user-friendly severity level name"""
        return {
            self.MINIMAL: "Very Low",
            self.MILD: "Low",
            self.MODERATE: "Moderate",
            self.MODERATELY_SEVERE: "Moderately High",
            self.SEVERE: "High",
            self.VERY_SEVERE: "Very High"
        }.get(self, "Unknown")


class QuestionType(Enum):
    """Types of assessment questions"""
    MULTIPLE_CHOICE = "multiple_choice"
    LIKERT_SCALE = "likert_scale"
    YES_NO = "yes_no"
    RATING_SCALE = "rating_scale"
    OPEN_ENDED = "open_ended"


@dataclass
class AssessmentQuestion:
    """Represents a single assessment question"""
    id: str
    text: str
    question_type: QuestionType
    options: List[str] = field(default_factory=list)
    scale_min: int = 0
    scale_max: int = 10
    required: bool = True
    cultural_adaptations: Dict[str, str] = field(default_factory=dict)
    explanation: str = ""  # Optional explanation for the question
    
    def get_culturally_adapted_text(self, culture: str) -> str:
        """Get culturally adapted question text"""
        return self.cultural_adaptations.get(culture, self.text)


@dataclass
class AssessmentResponse:
    """Represents a response to an assessment question"""
    question_id: str
    response: Union[str, int, float, bool]
    timestamp: datetime = field(default_factory=datetime.now)
    response_time_seconds: float = 0.0


@dataclass
class AssessmentResult:
    """Represents the result of a psychological assessment"""
    assessment_name: str
    user_friendly_name: str  # User-friendly name for display
    assessment_type: AssessmentType
    user_id: Optional[str]
    total_score: float
    max_possible_score: float
    severity_level: SeverityLevel
    percentile: Optional[float] = None
    subscale_scores: Dict[str, float] = field(default_factory=dict)
    responses: List[AssessmentResponse] = field(default_factory=list)
    interpretation: str = ""
    recommendations: List[str] = field(default_factory=list)
    cultural_context: Optional[str] = None
    completed_at: datetime = field(default_factory=datetime.now)
    completion_time_minutes: float = 0.0
    validity_flags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for storage"""
        return {
            'assessment_name': self.assessment_name,
            'user_friendly_name': self.user_friendly_name,
            'assessment_type': self.assessment_type.value,
            'user_id': self.user_id,
            'total_score': self.total_score,
            'max_possible_score': self.max_possible_score,
            'severity_level': self.severity_level.value,
            'severity_level_friendly': self.severity_level.user_friendly_name,
            'percentile': self.percentile,
            'subscale_scores': self.subscale_scores,
            'responses': [
                {
                    'question_id': r.question_id,
                    'response': r.response,
                    'timestamp': r.timestamp.isoformat(),
                    'response_time_seconds': r.response_time_seconds
                }
                for r in self.responses
            ],
            'interpretation': self.interpretation,
            'recommendations': self.recommendations,
            'cultural_context': self.cultural_context,
            'completed_at': self.completed_at.isoformat(),
            'completion_time_minutes': self.completion_time_minutes,
            'validity_flags': self.validity_flags
        }


class PsychologicalAssessment(ABC):
    """Abstract base class for psychological assessments"""
    
    def __init__(self, cultural_context: Optional[str] = None):
        self.cultural_context = cultural_context
        self.start_time: Optional[datetime] = None
        self.responses: List[AssessmentResponse] = []
        self.current_question_index = 0
        
    @property
    @abstractmethod
    def name(self) -> str:
        """Technical assessment name (internal use)"""
        pass
    
    @property
    @abstractmethod
    def user_friendly_name(self) -> str:
        """User-friendly assessment name (for display)"""
        pass
    
    @property
    @abstractmethod
    def assessment_type(self) -> AssessmentType:
        """Assessment type"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """User-friendly assessment description"""
        pass
    
    @property
    @abstractmethod
    def questions(self) -> List[AssessmentQuestion]:
        """List of assessment questions"""
        pass
    
    @property
    @abstractmethod
    def estimated_time_minutes(self) -> int:
        """Estimated time to complete assessment"""
        pass
    
    @property
    def total_questions(self) -> int:
        """Total number of questions in the assessment"""
        return len(self.questions)
    
    @property
    def is_complete(self) -> bool:
        """Check if assessment is complete"""
        return len(self.responses) == self.total_questions
    
    @property
    def progress_percentage(self) -> float:
        """Get completion progress as percentage"""
        if self.total_questions == 0:
            return 0.0
        return (len(self.responses) / self.total_questions) * 100
    
    def get_user_friendly_intro(self) -> str:
        """Get user-friendly introduction text"""
        return f"""
        Welcome to the {self.user_friendly_name}!
        
        This assessment helps us understand your current well-being and provide personalized support.
        
        • {self.total_questions} questions
        • Takes about {self.estimated_time_minutes} minutes
        • Your responses are completely confidential
        • There are no right or wrong answers
        
        Please answer honestly based on how you've been feeling recently.
        """
    
    def start_assessment(self, user_id: Optional[str] = None) -> None:
        """Start the assessment"""
        self.start_time = datetime.now()
        self.responses = []
        self.current_question_index = 0
        self.user_id = user_id
        logger.info(f"Started assessment: {self.user_friendly_name} ({self.name})")
    
    def get_next_question(self) -> Optional[AssessmentQuestion]:
        """Get the next question in the assessment"""
        if self.current_question_index >= len(self.questions):
            return None
        
        question = self.questions[self.current_question_index]
        
        # Apply cultural adaptations if available
        if self.cultural_context:
            adapted_text = question.get_culturally_adapted_text(self.cultural_context)
            if adapted_text != question.text:
                # Create a copy with adapted text
                question = AssessmentQuestion(
                    id=question.id,
                    text=adapted_text,
                    question_type=question.question_type,
                    options=question.options,
                    scale_min=question.scale_min,
                    scale_max=question.scale_max,
                    required=question.required,
                    cultural_adaptations=question.cultural_adaptations,
                    explanation=question.explanation
                )
        
        return question
    
    def submit_response(self, response: Union[str, int, float, bool], 
                       response_time_seconds: float = 0.0) -> bool:
        """Submit a response to the current question"""
        if self.current_question_index >= len(self.questions):
            return False
        
        current_question = self.questions[self.current_question_index]
        
        # Validate response
        if not self._validate_response(current_question, response):
            return False
        
        # Create response object
        assessment_response = AssessmentResponse(
            question_id=current_question.id,
            response=response,
            timestamp=datetime.now(),
            response_time_seconds=response_time_seconds
        )
        
        self.responses.append(assessment_response)
        self.current_question_index += 1
        
        return True
    
    def _validate_response(self, question: AssessmentQuestion, 
                          response: Union[str, int, float, bool]) -> bool:
        """Validate a response for a given question"""
        if question.required and response is None:
            return False
        
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            return str(response) in question.options
        elif question.question_type == QuestionType.LIKERT_SCALE:
            return isinstance(response, (int, float)) and question.scale_min <= response <= question.scale_max
        elif question.question_type == QuestionType.YES_NO:
            return isinstance(response, bool)
        elif question.question_type == QuestionType.RATING_SCALE:
            return isinstance(response, (int, float)) and question.scale_min <= response <= question.scale_max
        elif question.question_type == QuestionType.OPEN_ENDED:
            return isinstance(response, str)
        
        return True
    
    @abstractmethod
    def calculate_score(self) -> float:
        """Calculate the total score for the assessment"""
        pass
    
    @abstractmethod
    def get_severity_level(self, score: float) -> SeverityLevel:
        """Determine severity level based on score"""
        pass
    
    @abstractmethod
    def get_interpretation(self, score: float, severity: SeverityLevel) -> str:
        """Get user-friendly interpretation of the assessment results"""
        pass
    
    @abstractmethod
    def get_recommendations(self, score: float, severity: SeverityLevel) -> List[str]:
        """Get personalized recommendations based on assessment results"""
        pass
    
    def get_subscale_scores(self) -> Dict[str, float]:
        """Calculate subscale scores (override if assessment has subscales)"""
        return {}
    
    def get_percentile(self, score: float) -> Optional[float]:
        """Get percentile ranking for the score (override if normative data available)"""
        return None
    
    def validate_responses(self) -> List[str]:
        """Validate all responses and return any validity concerns"""
        validity_flags = []
        
        # Check for missing responses
        if len(self.responses) < self.total_questions:
            validity_flags.append("incomplete_assessment")
        
        # Check for response patterns that might indicate invalid responses
        response_values = [r.response for r in self.responses if isinstance(r.response, (int, float))]
        if response_values:
            # Check for straight-line responding (all same values)
            if len(set(response_values)) == 1:
                validity_flags.append("straight_line_responding")
            
            # Check for very fast responding (less than 3 seconds per question on average)
            total_time = sum(r.response_time_seconds for r in self.responses)
            if total_time > 0 and total_time / len(self.responses) < 3.0:
                validity_flags.append("rapid_responding")
        
        return validity_flags
    
    async def complete_assessment(self, user_id: Optional[str] = None) -> AssessmentResult:
        """Complete the assessment and return results"""
        if not self.is_complete:
            raise ValueError("Assessment is not complete")
        
        # Calculate scores
        total_score = self.calculate_score()
        severity_level = self.get_severity_level(total_score)
        subscale_scores = self.get_subscale_scores()
        percentile = self.get_percentile(total_score)
        
        # Get interpretation and recommendations
        interpretation = self.get_interpretation(total_score, severity_level)
        recommendations = self.get_recommendations(total_score, severity_level)
        
        # Calculate completion time
        completion_time = 0.0
        if self.start_time:
            completion_time = (datetime.now() - self.start_time).total_seconds() / 60.0
        
        # Validate responses
        validity_flags = self.validate_responses()
        
        # Create result object
        result = AssessmentResult(
            assessment_name=self.name,
            user_friendly_name=self.user_friendly_name,
            assessment_type=self.assessment_type,
            user_id=user_id,
            total_score=total_score,
            max_possible_score=self.get_max_possible_score(),
            severity_level=severity_level,
            percentile=percentile,
            subscale_scores=subscale_scores,
            responses=self.responses,
            interpretation=interpretation,
            recommendations=recommendations,
            cultural_context=self.cultural_context,
            completion_time_minutes=completion_time,
            validity_flags=validity_flags
        )
        
        logger.info(f"Completed assessment: {self.user_friendly_name}, Score: {total_score}, Severity: {severity_level.user_friendly_name}")
        
        return result
    
    @abstractmethod
    def get_max_possible_score(self) -> float:
        """Get the maximum possible score for this assessment"""
        pass
    
    def reset(self) -> None:
        """Reset the assessment to initial state"""
        self.start_time = None
        self.responses = []
        self.current_question_index = 0
        
    def get_progress_info(self) -> Dict[str, Any]:
        """Get current progress information"""
        return {
            'assessment_name': self.user_friendly_name,
            'current_question': self.current_question_index + 1,
            'total_questions': self.total_questions,
            'progress_percentage': self.progress_percentage,
            'responses_completed': len(self.responses),
            'is_complete': self.is_complete,
            'time_elapsed_minutes': (datetime.now() - self.start_time).total_seconds() / 60.0 if self.start_time else 0.0,
            'estimated_time_remaining': max(0, self.estimated_time_minutes - ((datetime.now() - self.start_time).total_seconds() / 60.0 if self.start_time else 0))
        }

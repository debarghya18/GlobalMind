"""
Custom exceptions for GlobalMind system
"""

from typing import Optional, Dict, Any


class GlobalMindException(Exception):
    """Base exception class for GlobalMind"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ConfigurationError(GlobalMindException):
    """Exception raised for configuration errors"""
    pass


class SecurityError(GlobalMindException):
    """Exception raised for security-related errors"""
    pass


class DatabaseError(GlobalMindException):
    """Exception raised for database-related errors"""
    pass


class TranslationError(GlobalMindException):
    """Exception raised for translation errors"""
    pass


class CulturalAdaptationError(GlobalMindException):
    """Raised when cultural adaptation fails"""
    pass


class VoiceProcessingError(GlobalMindException):
    """Raised when voice processing fails"""
    pass


class SMSServiceError(GlobalMindException):
    """Raised when SMS service fails"""
    pass


class AnalyticsError(GlobalMindException):
    """Raised when analytics operations fail"""
    pass


class ModelError(GlobalMindException):
    """Exception raised for AI model errors"""
    pass


class AuthenticationError(GlobalMindException):
    """Exception raised for authentication errors"""
    pass


class ValidationError(GlobalMindException):
    """Exception raised for validation errors"""
    pass


class CrisisDetectionError(GlobalMindException):
    """Exception raised for crisis detection errors"""
    pass


class PrivacyError(GlobalMindException):
    """Exception raised for privacy-related errors"""
    pass


class RateLimitError(GlobalMindException):
    """Exception raised for rate limiting errors"""
    pass


class ServiceUnavailableError(GlobalMindException):
    """Exception raised when service is unavailable"""
    pass


class InternalServerError(GlobalMindException):
    """Exception raised for internal server errors"""
    pass


# Error code mappings
ERROR_CODES = {
    'CONFIG_001': 'Configuration file not found',
    'CONFIG_002': 'Invalid configuration format',
    'CONFIG_003': 'Missing required configuration',
    'SEC_001': 'Encryption key not found',
    'SEC_002': 'Invalid encryption key format',
    'SEC_003': 'Authentication failed',
    'SEC_004': 'Authorization denied',
    'DB_001': 'Database connection failed',
    'DB_002': 'Database query failed',
    'DB_003': 'Database migration failed',
    'TRANS_001': 'Translation service unavailable',
    'TRANS_002': 'Unsupported language',
    'TRANS_003': 'Translation accuracy below threshold',
    'CULT_001': 'Cultural adaptation failed',
    'CULT_002': 'Cultural framework not found',
    'CULT_003': 'Regional adaptation unavailable',
    'MODEL_001': 'Model loading failed',
    'MODEL_002': 'Model inference failed',
    'MODEL_003': 'Model not found',
    'CRISIS_001': 'Crisis detection failed',
    'CRISIS_002': 'Emergency escalation failed',
    'PRIVACY_001': 'Data anonymization failed',
    'PRIVACY_002': 'Data encryption failed',
    'PRIVACY_003': 'Data deletion failed',
    'RATE_001': 'Rate limit exceeded',
    'RATE_002': 'Quota exceeded',
    'SVC_001': 'Service temporarily unavailable',
    'SVC_002': 'Service maintenance mode',
    'INT_001': 'Internal server error',
    'INT_002': 'Unexpected error occurred'
}


def get_error_message(error_code: str) -> str:
    """Get error message for error code"""
    return ERROR_CODES.get(error_code, 'Unknown error')


def create_exception(error_code: str, message: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> GlobalMindException:
    """Create exception instance from error code"""
    if not message:
        message = get_error_message(error_code)
    
    # Map error codes to exception classes
    if error_code.startswith('CONFIG_'):
        return ConfigurationError(message, error_code, details)
    elif error_code.startswith('SEC_'):
        return SecurityError(message, error_code, details)
    elif error_code.startswith('DB_'):
        return DatabaseError(message, error_code, details)
    elif error_code.startswith('TRANS_'):
        return TranslationError(message, error_code, details)
    elif error_code.startswith('CULT_'):
        return CulturalAdaptationError(message, error_code, details)
    elif error_code.startswith('MODEL_'):
        return ModelError(message, error_code, details)
    elif error_code.startswith('CRISIS_'):
        return CrisisDetectionError(message, error_code, details)
    elif error_code.startswith('PRIVACY_'):
        return PrivacyError(message, error_code, details)
    elif error_code.startswith('RATE_'):
        return RateLimitError(message, error_code, details)
    elif error_code.startswith('SVC_'):
        return ServiceUnavailableError(message, error_code, details)
    elif error_code.startswith('INT_'):
        return InternalServerError(message, error_code, details)
    else:
        return GlobalMindException(message, error_code, details)

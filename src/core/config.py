"""
Configuration management module for GlobalMind
Handles loading and validation of configuration settings
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class AppConfig:
    """Application configuration"""
    name: str
    version: str
    description: str
    debug: bool
    host: str
    port: int


@dataclass
class SecurityConfig:
    """Security configuration"""
    encryption_algorithm: str
    key_rotation_days: int
    anonymize_data: bool
    data_retention_days: int
    gdpr_compliance: bool
    hipaa_compliance: bool
    delete_on_request: bool
    session_timeout: int
    max_sessions: int
    require_2fa: bool


@dataclass
class DatabaseConfig:
    """Database configuration"""
    type: str
    path: str
    backup_enabled: bool
    backup_interval: int
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: Optional[str]


@dataclass
class ModelsConfig:
    """AI models configuration"""
    translation_model: str
    sentiment_model: str
    cultural_model: str
    embedding_model: str
    cbt_model: str
    mindfulness_model: str
    crisis_detection_model: str
    offline_enabled: bool
    offline_models_path: str
    offline_max_size_mb: int


@dataclass
class PerformanceConfig:
    """Performance metrics configuration"""
    translation_accuracy_threshold: float
    cultural_appropriateness_threshold: float
    user_satisfaction_threshold: float
    offline_availability_threshold: float
    response_time_threshold: float


@dataclass
class MonitoringConfig:
    """Monitoring configuration"""
    enabled: bool
    log_level: str
    log_file: str
    metrics_port: int
    email_notifications: bool
    slack_webhook: Optional[str]
    performance_degradation: bool
    security_incidents: bool


@dataclass
class EmergencyConfig:
    """Emergency protocols configuration"""
    crisis_keywords: list
    escalation_enabled: bool
    hotline_numbers: Dict[str, str]
    priority_routing: bool
    human_handoff: bool
    emergency_contacts: bool


@dataclass
class GlobalMindConfig:
    """Main configuration class"""
    app: AppConfig
    security: SecurityConfig
    database: DatabaseConfig
    models: ModelsConfig
    performance: PerformanceConfig
    monitoring: MonitoringConfig
    emergency: EmergencyConfig
    supported_languages: list
    default_language: str
    fallback_language: str
    auto_detect: bool
    cultural_frameworks: list
    regional_adaptations: Dict[str, list]
    raw_config: Dict[str, Any]


def load_config(config_path: Optional[str] = None) -> GlobalMindConfig:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file (optional)
        
    Returns:
        GlobalMindConfig: Loaded configuration
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    
    logger.info(f"Loading configuration from {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
        
        # Load app configuration
        app_config = AppConfig(
            name=config_data['app']['name'],
            version=config_data['app']['version'],
            description=config_data['app']['description'],
            debug=config_data['app']['debug'],
            host=config_data['app']['host'],
            port=config_data['app']['port']
        )
        
        # Load security configuration
        security_config = SecurityConfig(
            encryption_algorithm=config_data['security']['encryption']['algorithm'],
            key_rotation_days=config_data['security']['encryption']['key_rotation_days'],
            anonymize_data=config_data['security']['privacy']['anonymize_data'],
            data_retention_days=config_data['security']['privacy']['data_retention_days'],
            gdpr_compliance=config_data['security']['privacy']['gdpr_compliance'],
            hipaa_compliance=config_data['security']['privacy']['hipaa_compliance'],
            delete_on_request=config_data['security']['privacy']['delete_on_request'],
            session_timeout=config_data['security']['authentication']['session_timeout'],
            max_sessions=config_data['security']['authentication']['max_sessions'],
            require_2fa=config_data['security']['authentication']['require_2fa']
        )
        
        # Load database configuration
        database_config = DatabaseConfig(
            type=config_data['database']['type'],
            path=config_data['database']['path'],
            backup_enabled=config_data['database']['backup_enabled'],
            backup_interval=config_data['database']['backup_interval'],
            redis_host=config_data['database']['redis']['host'],
            redis_port=config_data['database']['redis']['port'],
            redis_db=config_data['database']['redis']['db'],
            redis_password=config_data['database']['redis']['password']
        )
        
        # Load models configuration
        models_config = ModelsConfig(
            translation_model=config_data['models']['nlp']['translation_model'],
            sentiment_model=config_data['models']['nlp']['sentiment_model'],
            cultural_model=config_data['models']['nlp']['cultural_model'],
            embedding_model=config_data['models']['nlp']['embedding_model'],
            cbt_model=config_data['models']['therapy']['cbt_model'],
            mindfulness_model=config_data['models']['therapy']['mindfulness_model'],
            crisis_detection_model=config_data['models']['therapy']['crisis_detection_model'],
            offline_enabled=config_data['models']['offline']['enabled'],
            offline_models_path=config_data['models']['offline']['models_path'],
            offline_max_size_mb=config_data['models']['offline']['max_size_mb']
        )
        
        # Load performance configuration
        performance_config = PerformanceConfig(
            translation_accuracy_threshold=config_data['performance']['translation_accuracy_threshold'],
            cultural_appropriateness_threshold=config_data['performance']['cultural_appropriateness_threshold'],
            user_satisfaction_threshold=config_data['performance']['user_satisfaction_threshold'],
            offline_availability_threshold=config_data['performance']['offline_availability_threshold'],
            response_time_threshold=config_data['performance']['response_time_threshold']
        )
        
        # Load monitoring configuration
        monitoring_config = MonitoringConfig(
            enabled=config_data['monitoring']['enabled'],
            log_level=config_data['monitoring']['log_level'],
            log_file=config_data['monitoring']['log_file'],
            metrics_port=config_data['monitoring']['metrics_port'],
            email_notifications=config_data['monitoring']['alerts']['email_notifications'],
            slack_webhook=config_data['monitoring']['alerts']['slack_webhook'],
            performance_degradation=config_data['monitoring']['alerts']['performance_degradation'],
            security_incidents=config_data['monitoring']['alerts']['security_incidents']
        )
        
        # Load emergency configuration
        emergency_config = EmergencyConfig(
            crisis_keywords=config_data['emergency']['crisis_keywords'],
            escalation_enabled=config_data['emergency']['escalation']['enabled'],
            hotline_numbers=config_data['emergency']['escalation']['hotline_numbers'],
            priority_routing=config_data['emergency']['immediate_response']['priority_routing'],
            human_handoff=config_data['emergency']['immediate_response']['human_handoff'],
            emergency_contacts=config_data['emergency']['immediate_response']['emergency_contacts']
        )
        
        # Create main configuration object
        config = GlobalMindConfig(
            app=app_config,
            security=security_config,
            database=database_config,
            models=models_config,
            performance=performance_config,
            monitoring=monitoring_config,
            emergency=emergency_config,
            supported_languages=config_data['languages']['supported_languages'],
            default_language=config_data['languages']['default_language'],
            fallback_language=config_data['languages']['fallback_language'],
            auto_detect=config_data['languages']['auto_detect'],
            cultural_frameworks=config_data['cultural']['frameworks'],
            regional_adaptations=config_data['cultural']['regional_adaptations'],
            raw_config=config_data
        )
        
        logger.info("Configuration loaded successfully")
        return config
        
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        raise
    except KeyError as e:
        logger.error(f"Missing required configuration key: {e}")
        raise


def validate_config(config: GlobalMindConfig) -> bool:
    """
    Validate configuration settings
    
    Args:
        config: Configuration to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    logger.info("Validating configuration")
    
    # Validate language settings
    if config.default_language not in config.supported_languages:
        logger.error(f"Default language '{config.default_language}' not in supported languages")
        return False
    
    if config.fallback_language not in config.supported_languages:
        logger.error(f"Fallback language '{config.fallback_language}' not in supported languages")
        return False
    
    # Validate performance thresholds
    if not (0.0 <= config.performance.translation_accuracy_threshold <= 1.0):
        logger.error("Translation accuracy threshold must be between 0.0 and 1.0")
        return False
    
    if not (0.0 <= config.performance.cultural_appropriateness_threshold <= 1.0):
        logger.error("Cultural appropriateness threshold must be between 0.0 and 1.0")
        return False
    
    if not (0.0 <= config.performance.user_satisfaction_threshold <= 5.0):
        logger.error("User satisfaction threshold must be between 0.0 and 5.0")
        return False
    
    # Validate database configuration
    if config.database.type not in ['sqlite', 'postgresql', 'mysql']:
        logger.error(f"Unsupported database type: {config.database.type}")
        return False
    
    logger.info("Configuration validation passed")
    return True


def get_environment_config() -> Dict[str, Any]:
    """
    Get configuration overrides from environment variables
    
    Returns:
        Dict[str, Any]: Environment configuration
    """
    env_config = {}
    
    # Database configuration
    if os.getenv('GLOBALMIND_DB_TYPE'):
        env_config['database_type'] = os.getenv('GLOBALMIND_DB_TYPE')
    
    if os.getenv('GLOBALMIND_DB_PATH'):
        env_config['database_path'] = os.getenv('GLOBALMIND_DB_PATH')
    
    if os.getenv('GLOBALMIND_REDIS_HOST'):
        env_config['redis_host'] = os.getenv('GLOBALMIND_REDIS_HOST')
    
    if os.getenv('GLOBALMIND_REDIS_PORT'):
        env_config['redis_port'] = int(os.getenv('GLOBALMIND_REDIS_PORT'))
    
    # Security configuration
    if os.getenv('GLOBALMIND_ENCRYPTION_KEY'):
        env_config['encryption_key'] = os.getenv('GLOBALMIND_ENCRYPTION_KEY')
    
    # API configuration
    if os.getenv('GLOBALMIND_API_HOST'):
        env_config['api_host'] = os.getenv('GLOBALMIND_API_HOST')
    
    if os.getenv('GLOBALMIND_API_PORT'):
        env_config['api_port'] = int(os.getenv('GLOBALMIND_API_PORT'))
    
    # Model configuration
    if os.getenv('GLOBALMIND_MODELS_PATH'):
        env_config['models_path'] = os.getenv('GLOBALMIND_MODELS_PATH')
    
    return env_config

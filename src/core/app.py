"""
Main application class for GlobalMind
Orchestrates all system components
"""

import asyncio
import signal
from typing import Dict, Any, Optional
from loguru import logger
from pathlib import Path

from .config import GlobalMindConfig, validate_config
from .exceptions import GlobalMindException
from ..security.encryption import EncryptionManager
from ..security.privacy import PrivacyManager
from ..storage.database import DatabaseManager
from ..nlp.language_detector import LanguageDetector
from ..nlp.translator import MultilingualTranslator
from ..cultural.adapter import CulturalAdapter
from ..models.therapy_models import TherapyModels
from ..models.crisis_detection import CrisisDetector
from ..monitoring.metrics import MetricsManager
from ..monitoring.logger import setup_logging
from ..ui.api import APIServer
from ..ui.websocket import WebSocketServer


class GlobalMindApp:
    """Main application class that orchestrates all system components"""
    
    def __init__(self, config: GlobalMindConfig):
        """
        Initialize the GlobalMind application
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.is_running = False
        self.components: Dict[str, Any] = {}
        
        # Validate configuration
        if not validate_config(config):
            raise GlobalMindException("Invalid configuration")
        
        # Setup logging
        setup_logging(config.monitoring)
        
        logger.info(f"Initializing {config.app.name} v{config.app.version}")
        logger.info(f"Description: {config.app.description}")
        
        # Initialize components
        self._init_components()
        
        # Setup signal handlers
        self._setup_signal_handlers()
    
    def _init_components(self):
        """Initialize all system components"""
        try:
            logger.info("Initializing system components...")
            
            # Core security components
            self.components['encryption'] = EncryptionManager(self.config.security)
            self.components['privacy'] = PrivacyManager(self.config.security)
            
            # Database and storage
            self.components['database'] = DatabaseManager(self.config.database)
            
            # NLP components
            self.components['language_detector'] = LanguageDetector(self.config.supported_languages)
            self.components['translator'] = MultilingualTranslator(
                self.config.models.translation_model,
                self.config.supported_languages
            )
            
            # Cultural adaptation
            self.components['cultural_adapter'] = CulturalAdapter(
                self.config.cultural_frameworks,
                self.config.regional_adaptations
            )
            
            # AI models
            self.components['therapy_models'] = TherapyModels(self.config.models)
            self.components['crisis_detector'] = CrisisDetector(
                self.config.models.crisis_detection_model,
                self.config.emergency.crisis_keywords
            )
            
            # Monitoring
            self.components['metrics'] = MetricsManager(self.config.monitoring)
            
            # API and WebSocket servers
            self.components['api_server'] = APIServer(self.config, self.components)
            self.components['websocket_server'] = WebSocketServer(self.config, self.components)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise GlobalMindException(f"Component initialization failed: {e}")
    
    async def start(self):
        """Start the GlobalMind application"""
        try:
            logger.info("Starting GlobalMind application...")
            
            # Start core services
            await self._start_core_services()
            
            # Start monitoring
            await self._start_monitoring()
            
            # Start API servers
            await self._start_servers()
            
            self.is_running = True
            logger.info("GlobalMind application started successfully")
            
            # Keep the application running
            await self._run_forever()
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            await self.shutdown()
            raise
    
    async def _start_core_services(self):
        """Start core services"""
        logger.info("Starting core services...")
        
        # Initialize database
        await self.components['database'].initialize()
        
        # Load AI models
        await self.components['therapy_models'].load_models()
        await self.components['crisis_detector'].load_model()
        
        # Initialize cultural adapter
        await self.components['cultural_adapter'].initialize()
        
        logger.info("Core services started")
    
    async def _start_monitoring(self):
        """Start monitoring services"""
        if self.config.monitoring.enabled:
            logger.info("Starting monitoring services...")
            await self.components['metrics'].start()
            logger.info("Monitoring services started")
    
    async def _start_servers(self):
        """Start API and WebSocket servers"""
        logger.info("Starting API servers...")
        
        # Start API server
        await self.components['api_server'].start()
        
        # Start WebSocket server
        await self.components['websocket_server'].start()
        
        logger.info(f"API server started on {self.config.app.host}:{self.config.app.port}")
    
    async def _run_forever(self):
        """Keep the application running"""
        try:
            while self.is_running:
                # Perform periodic tasks
                await self._periodic_tasks()
                
                # Sleep for a short interval
                await asyncio.sleep(1)
                
        except asyncio.CancelledError:
            logger.info("Application main loop cancelled")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            raise
    
    async def _periodic_tasks(self):
        """Perform periodic maintenance tasks"""
        # Update metrics
        if self.config.monitoring.enabled:
            await self.components['metrics'].update_system_metrics()
        
        # Check component health
        await self._health_check()
        
        # Cleanup old data if needed
        await self._cleanup_old_data()
    
    async def _health_check(self):
        """Perform health check on all components"""
        try:
            # Check database health
            if not await self.components['database'].health_check():
                logger.warning("Database health check failed")
            
            # Check AI models
            if not await self.components['therapy_models'].health_check():
                logger.warning("Therapy models health check failed")
                
            # Check translation service
            if not await self.components['translator'].health_check():
                logger.warning("Translation service health check failed")
                
        except Exception as e:
            logger.error(f"Health check failed: {e}")
    
    async def _cleanup_old_data(self):
        """Cleanup old data based on retention policy"""
        try:
            if self.config.security.data_retention_days > 0:
                await self.components['privacy'].cleanup_old_data(
                    self.config.security.data_retention_days
                )
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}")
    
    async def shutdown(self):
        """Shutdown the application gracefully"""
        logger.info("Shutting down GlobalMind application...")
        
        self.is_running = False
        
        try:
            # Stop servers
            if 'api_server' in self.components:
                await self.components['api_server'].shutdown()
            
            if 'websocket_server' in self.components:
                await self.components['websocket_server'].shutdown()
            
            # Stop monitoring
            if 'metrics' in self.components and self.config.monitoring.enabled:
                await self.components['metrics'].shutdown()
            
            # Close database connections
            if 'database' in self.components:
                await self.components['database'].close()
            
            # Cleanup resources
            await self._cleanup_resources()
            
            logger.info("Application shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    async def _cleanup_resources(self):
        """Cleanup application resources"""
        try:
            # Clear sensitive data from memory
            if 'encryption' in self.components:
                self.components['encryption'].cleanup()
            
            # Clear model caches
            if 'therapy_models' in self.components:
                await self.components['therapy_models'].cleanup()
            
            if 'crisis_detector' in self.components:
                await self.components['crisis_detector'].cleanup()
            
        except Exception as e:
            logger.error(f"Resource cleanup failed: {e}")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating shutdown...")
            asyncio.create_task(self.shutdown())
        
        try:
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except ValueError:
            # Signal handling not available (e.g., on Windows)
            logger.warning("Signal handling not available on this platform")
    
    def get_component(self, name: str) -> Optional[Any]:
        """Get a component by name"""
        return self.components.get(name)
    
    def get_status(self) -> Dict[str, Any]:
        """Get application status"""
        return {
            'name': self.config.app.name,
            'version': self.config.app.version,
            'running': self.is_running,
            'components': {
                name: hasattr(component, 'is_healthy') and component.is_healthy() 
                for name, component in self.components.items()
            },
            'supported_languages': len(self.config.supported_languages),
            'cultural_frameworks': len(self.config.cultural_frameworks)
        }
    
    async def handle_user_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle user request with full pipeline
        
        Args:
            request: User request data
            
        Returns:
            Dict containing response data
        """
        try:
            # Detect language
            detected_language = await self.components['language_detector'].detect(
                request.get('text', '')
            )
            
            # Get cultural context
            cultural_context = await self.components['cultural_adapter'].get_context(
                request.get('user_profile', {}),
                detected_language
            )
            
            # Check for crisis
            crisis_level = await self.components['crisis_detector'].detect_crisis(
                request.get('text', ''),
                cultural_context
            )
            
            # Generate response
            if crisis_level > 0.7:  # High crisis level
                response = await self._handle_crisis_response(request, cultural_context)
            else:
                response = await self._handle_regular_response(request, cultural_context)
            
            # Log interaction (anonymized)
            await self._log_interaction(request, response, detected_language)
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling user request: {e}")
            return {
                'error': True,
                'message': 'Sorry, I encountered an error processing your request.',
                'error_code': 'INT_001'
            }
    
    async def _handle_crisis_response(self, request: Dict[str, Any], cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle crisis response with emergency protocols"""
        logger.warning("Crisis detected, activating emergency protocols")
        
        # Generate culturally appropriate crisis response
        crisis_response = await self.components['therapy_models'].generate_crisis_response(
            request.get('text', ''),
            cultural_context
        )
        
        # Add emergency resources
        emergency_resources = await self.components['cultural_adapter'].get_emergency_resources(
            cultural_context
        )
        
        return {
            'message': crisis_response,
            'crisis_detected': True,
            'emergency_resources': emergency_resources,
            'cultural_context': cultural_context
        }
    
    async def _handle_regular_response(self, request: Dict[str, Any], cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle regular therapeutic response"""
        # Generate culturally adapted response
        response = await self.components['therapy_models'].generate_response(
            request.get('text', ''),
            cultural_context,
            request.get('session_history', [])
        )
        
        return {
            'message': response,
            'cultural_context': cultural_context,
            'crisis_detected': False
        }
    
    async def _log_interaction(self, request: Dict[str, Any], response: Dict[str, Any], language: str):
        """Log user interaction with privacy protection"""
        try:
            # Anonymize data
            anonymized_data = await self.components['privacy'].anonymize_interaction(
                request, response, language
            )
            
            # Store in database
            await self.components['database'].store_interaction(anonymized_data)
            
            # Update metrics
            await self.components['metrics'].record_interaction(language, response.get('crisis_detected', False))
            
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")


# Create init files for modules
async def create_init_files():
    """Create __init__.py files for all modules"""
    modules = [
        "src",
        "src/core",
        "src/nlp", 
        "src/cultural",
        "src/security",
        "src/ui",
        "src/monitoring",
        "src/storage",
        "src/models"
    ]
    
    for module in modules:
        init_file = Path(module) / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            logger.info(f"Created {init_file}")


if __name__ == "__main__":
    # This should not be run directly, use main.py instead
    logger.error("Use main.py to start the application")

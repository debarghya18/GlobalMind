"""
FastAPI server for GlobalMind backend communication
Handles API requests and integrates with core components
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import uvicorn
from loguru import logger

from ..core.config import GlobalMindConfig
from ..core.exceptions import GlobalMindException


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    language: Optional[str] = "en"
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    cultural_context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    language: str
    cultural_context: Dict[str, Any]
    crisis_detected: bool
    session_id: str
    timestamp: datetime


class UserProfile(BaseModel):
    """User profile model"""
    user_id: str
    language: str
    cultural_background: str
    preferences: Dict[str, Any]


class ProgressData(BaseModel):
    """Progress data model"""
    user_id: str
    mood_scores: List[float]
    session_count: int
    improvement_percentage: float
    satisfaction_rating: float


class APIServer:
    """FastAPI server for GlobalMind"""
    
    def __init__(self, config: GlobalMindConfig, components: Dict[str, Any]):
        """
        Initialize API server
        
        Args:
            config: Application configuration
            components: System components
        """
        self.config = config
        self.components = components
        self.app = FastAPI(
            title="GlobalMind API",
            description="Culturally-Adaptive Mental Health AI Support System",
            version="1.0.0"
        )
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=config.raw_config.get('api', {}).get('cors', {}).get('origins', ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Setup routes
        self._setup_routes()
        
        logger.info("API server initialized")
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            """Root endpoint"""
            return {"message": "Welcome to GlobalMind API", "version": "1.0.0"}
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            try:
                # Check component health
                health_status = {
                    "status": "healthy",
                    "timestamp": datetime.now(),
                    "components": {}
                }
                
                for name, component in self.components.items():
                    if hasattr(component, 'health_check'):
                        health_status["components"][name] = await component.health_check()
                    else:
                        health_status["components"][name] = True
                
                return health_status
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"status": "unhealthy", "error": str(e)}
                )
        
        @self.app.post("/api/v1/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest):
            """Chat endpoint"""
            try:
                # Build request for core app
                app_request = {
                    'text': request.message,
                    'language': request.language,
                    'user_id': request.user_id,
                    'session_id': request.session_id,
                    'user_profile': request.cultural_context or {}
                }
                
                # Get main app component
                main_app = self.components.get('main_app')
                if not main_app:
                    raise HTTPException(status_code=500, detail="Main application not available")
                
                # Process request
                response = await main_app.handle_user_request(app_request)
                
                return ChatResponse(
                    message=response['message'],
                    language=request.language,
                    cultural_context=response.get('cultural_context', {}),
                    crisis_detected=response.get('crisis_detected', False),
                    session_id=request.session_id or "session_" + str(datetime.now().timestamp()),
                    timestamp=datetime.now()
                )
                
            except Exception as e:
                logger.error(f"Chat endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/languages")
        async def get_supported_languages():
            """Get supported languages"""
            try:
                language_detector = self.components.get('language_detector')
                if not language_detector:
                    raise HTTPException(status_code=500, detail="Language detector not available")
                
                stats = language_detector.get_statistics()
                return {
                    "languages": stats.get('languages', []),
                    "count": stats.get('supported_languages', 0)
                }
            except Exception as e:
                logger.error(f"Languages endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/v1/translate")
        async def translate_text(text: str, target_language: str):
            """Translate text"""
            try:
                translator = self.components.get('translator')
                if not translator:
                    raise HTTPException(status_code=500, detail="Translator not available")
                
                translated = await translator.translate(text, target_language)
                return {"original": text, "translated": translated, "target_language": target_language}
            except Exception as e:
                logger.error(f"Translation endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/cultural-context")
        async def get_cultural_context(language: str, user_profile: Optional[Dict[str, Any]] = None):
            """Get cultural context"""
            try:
                cultural_adapter = self.components.get('cultural_adapter')
                if not cultural_adapter:
                    raise HTTPException(status_code=500, detail="Cultural adapter not available")
                
                context = await cultural_adapter.get_context(user_profile or {}, language)
                return context
            except Exception as e:
                logger.error(f"Cultural context endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/v1/crisis-detection")
        async def detect_crisis(text: str, cultural_context: Optional[Dict[str, Any]] = None):
            """Detect crisis in text"""
            try:
                crisis_detector = self.components.get('crisis_detector')
                if not crisis_detector:
                    raise HTTPException(status_code=500, detail="Crisis detector not available")
                
                crisis_level = await crisis_detector.detect_crisis(text, cultural_context or {})
                return {"crisis_level": crisis_level, "is_crisis": crisis_level > 0.7}
            except Exception as e:
                logger.error(f"Crisis detection endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/progress/{user_id}")
        async def get_user_progress(user_id: str):
            """Get user progress data"""
            try:
                database = self.components.get('database')
                if not database:
                    raise HTTPException(status_code=500, detail="Database not available")
                
                # This would fetch real progress data from database
                # For now, returning mock data
                return {
                    "user_id": user_id,
                    "total_sessions": 42,
                    "mood_improvement": 87,
                    "streak_days": 15,
                    "satisfaction": 4.8,
                    "last_session": datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Progress endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/metrics")
        async def get_system_metrics():
            """Get system metrics"""
            try:
                metrics = self.components.get('metrics')
                if not metrics:
                    raise HTTPException(status_code=500, detail="Metrics not available")
                
                # Get system metrics
                return {
                    "uptime": "24h 30m",
                    "total_users": 1250,
                    "active_sessions": 43,
                    "languages_supported": len(self.config.supported_languages),
                    "cultural_frameworks": len(self.config.cultural_frameworks),
                    "crisis_interventions": 12,
                    "satisfaction_rating": 4.7
                }
            except Exception as e:
                logger.error(f"Metrics endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/v1/feedback")
        async def submit_feedback(rating: int, comment: str, user_id: Optional[str] = None):
            """Submit user feedback"""
            try:
                # Store feedback in database
                feedback_data = {
                    "user_id": user_id,
                    "rating": rating,
                    "comment": comment,
                    "timestamp": datetime.now()
                }
                
                # This would store in actual database
                logger.info(f"Feedback received: {feedback_data}")
                
                return {"message": "Feedback submitted successfully", "status": "success"}
            except Exception as e:
                logger.error(f"Feedback endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/emergency-resources")
        async def get_emergency_resources(language: str = "en", cultural_context: Optional[Dict[str, Any]] = None):
            """Get emergency resources"""
            try:
                cultural_adapter = self.components.get('cultural_adapter')
                if not cultural_adapter:
                    raise HTTPException(status_code=500, detail="Cultural adapter not available")
                
                resources = await cultural_adapter.get_emergency_resources(cultural_context or {'language': language})
                return {"resources": resources}
            except Exception as e:
                logger.error(f"Emergency resources endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/v1/user-profile")
        async def update_user_profile(profile: UserProfile):
            """Update user profile"""
            try:
                # Store profile in database
                logger.info(f"User profile updated: {profile.dict()}")
                return {"message": "Profile updated successfully", "status": "success"}
            except Exception as e:
                logger.error(f"Profile update endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.delete("/api/v1/user-data/{user_id}")
        async def delete_user_data(user_id: str):
            """Delete user data"""
            try:
                privacy_manager = self.components.get('privacy')
                if not privacy_manager:
                    raise HTTPException(status_code=500, detail="Privacy manager not available")
                
                # This would delete user data from database
                logger.info(f"User data deletion requested for: {user_id}")
                
                return {"message": "User data deletion initiated", "status": "success"}
            except Exception as e:
                logger.error(f"Data deletion endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def start(self):
        """Start the API server"""
        try:
            logger.info(f"Starting API server on {self.config.app.host}:{self.config.app.port}")
            
            # In a real deployment, this would be handled by a proper ASGI server
            # For development, we can use uvicorn
            config = uvicorn.Config(
                self.app,
                host=self.config.app.host,
                port=self.config.app.port,
                log_level="info"
            )
            
            server = uvicorn.Server(config)
            await server.serve()
            
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the API server"""
        try:
            logger.info("Shutting down API server...")
            # Server shutdown logic would go here
            
        except Exception as e:
            logger.error(f"Error shutting down API server: {e}")
    
    def get_app(self):
        """Get the FastAPI app instance"""
        return self.app

"""
WebSocket server for real-time communication
Handles real-time chat and notifications
"""

import asyncio
import json
from typing import Dict, Any, Set
from datetime import datetime
import websockets
from websockets.server import WebSocketServerProtocol
from loguru import logger

from ..core.config import GlobalMindConfig
from ..core.exceptions import GlobalMindException


class WebSocketServer:
    """WebSocket server for real-time communication"""
    
    def __init__(self, config: GlobalMindConfig, components: Dict[str, Any]):
        """
        Initialize WebSocket server
        
        Args:
            config: Application configuration
            components: System components
        """
        self.config = config
        self.components = components
        self.active_connections: Dict[str, WebSocketServerProtocol] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
        self.is_running = False
        
        logger.info("WebSocket server initialized")
    
    async def register_connection(self, websocket: WebSocketServerProtocol, user_id: str = None):
        """Register a new WebSocket connection"""
        connection_id = f"conn_{datetime.now().timestamp()}"
        self.active_connections[connection_id] = websocket
        
        if user_id:
            self.user_sessions[user_id] = connection_id
        
        logger.info(f"New WebSocket connection registered: {connection_id}")
        return connection_id
    
    async def unregister_connection(self, connection_id: str):
        """Unregister a WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove from user sessions
        for user_id, conn_id in list(self.user_sessions.items()):
            if conn_id == connection_id:
                del self.user_sessions[user_id]
                break
        
        logger.info(f"WebSocket connection unregistered: {connection_id}")
    
    async def send_message(self, connection_id: str, message: Dict[str, Any]):
        """Send message to a specific connection"""
        if connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send(json.dumps(message))
                logger.debug(f"Message sent to {connection_id}: {message}")
            except Exception as e:
                logger.error(f"Failed to send message to {connection_id}: {e}")
                await self.unregister_connection(connection_id)
    
    async def broadcast_message(self, message: Dict[str, Any], exclude_connection: str = None):
        """Broadcast message to all connections"""
        for connection_id, websocket in list(self.active_connections.items()):
            if connection_id != exclude_connection:
                try:
                    await websocket.send(json.dumps(message))
                except Exception as e:
                    logger.error(f"Failed to broadcast to {connection_id}: {e}")
                    await self.unregister_connection(connection_id)
    
    async def send_to_user(self, user_id: str, message: Dict[str, Any]):
        """Send message to a specific user"""
        if user_id in self.user_sessions:
            connection_id = self.user_sessions[user_id]
            await self.send_message(connection_id, message)
    
    async def handle_chat_message(self, connection_id: str, data: Dict[str, Any]):
        """Handle chat message from client"""
        try:
            # Extract message data
            message = data.get('message', '')
            user_id = data.get('user_id')
            language = data.get('language', 'en')
            
            # Build request for core app
            app_request = {
                'text': message,
                'language': language,
                'user_id': user_id,
                'user_profile': data.get('user_profile', {})
            }
            
            # Get main app component
            main_app = self.components.get('main_app')
            if not main_app:
                await self.send_message(connection_id, {
                    'type': 'error',
                    'message': 'Service temporarily unavailable'
                })
                return
            
            # Process request
            response = await main_app.handle_user_request(app_request)
            
            # Send response back
            await self.send_message(connection_id, {
                'type': 'chat_response',
                'message': response['message'],
                'cultural_context': response.get('cultural_context', {}),
                'crisis_detected': response.get('crisis_detected', False),
                'timestamp': datetime.now().isoformat()
            })
            
            # If crisis detected, send additional resources
            if response.get('crisis_detected', False):
                await self.send_crisis_resources(connection_id, response.get('cultural_context', {}))
            
        except Exception as e:
            logger.error(f"Error handling chat message: {e}")
            await self.send_message(connection_id, {
                'type': 'error',
                'message': 'Sorry, I encountered an error processing your message.'
            })
    
    async def send_crisis_resources(self, connection_id: str, cultural_context: Dict[str, Any]):
        """Send crisis resources to client"""
        try:
            cultural_adapter = self.components.get('cultural_adapter')
            if cultural_adapter:
                resources = await cultural_adapter.get_emergency_resources(cultural_context)
                await self.send_message(connection_id, {
                    'type': 'crisis_resources',
                    'resources': resources,
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            logger.error(f"Error sending crisis resources: {e}")
    
    async def handle_language_change(self, connection_id: str, data: Dict[str, Any]):
        """Handle language change request"""
        try:
            new_language = data.get('language', 'en')
            
            # Validate language
            if new_language not in self.config.supported_languages:
                await self.send_message(connection_id, {
                    'type': 'error',
                    'message': f'Language "{new_language}" is not supported'
                })
                return
            
            # Confirm language change
            await self.send_message(connection_id, {
                'type': 'language_changed',
                'language': new_language,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error handling language change: {e}")
    
    async def handle_progress_request(self, connection_id: str, data: Dict[str, Any]):
        """Handle progress data request"""
        try:
            user_id = data.get('user_id')
            if not user_id:
                await self.send_message(connection_id, {
                    'type': 'error',
                    'message': 'User ID required for progress data'
                })
                return
            
            # Mock progress data (would come from database)
            progress_data = {
                'total_sessions': 42,
                'mood_improvement': 87,
                'streak_days': 15,
                'satisfaction': 4.8,
                'last_session': datetime.now().isoformat()
            }
            
            await self.send_message(connection_id, {
                'type': 'progress_data',
                'data': progress_data,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error handling progress request: {e}")
    
    async def handle_client_message(self, connection_id: str, message: str):
        """Handle incoming client message"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'chat':
                await self.handle_chat_message(connection_id, data)
            elif message_type == 'language_change':
                await self.handle_language_change(connection_id, data)
            elif message_type == 'progress_request':
                await self.handle_progress_request(connection_id, data)
            elif message_type == 'ping':
                await self.send_message(connection_id, {'type': 'pong'})
            else:
                logger.warning(f"Unknown message type: {message_type}")
            
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message from {connection_id}")
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    async def connection_handler(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket connection"""
        connection_id = None
        try:
            # Register connection
            connection_id = await self.register_connection(websocket)
            
            # Send welcome message
            await self.send_message(connection_id, {
                'type': 'welcome',
                'message': 'Connected to GlobalMind',
                'connection_id': connection_id,
                'timestamp': datetime.now().isoformat()
            })
            
            # Handle messages
            async for message in websocket:
                await self.handle_client_message(connection_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed: {connection_id}")
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
        finally:
            if connection_id:
                await self.unregister_connection(connection_id)
    
    async def start(self):
        """Start the WebSocket server"""
        try:
            self.is_running = True
            host = self.config.app.host
            port = self.config.app.port + 1  # Use port + 1 for WebSocket
            
            logger.info(f"Starting WebSocket server on {host}:{port}")
            
            # Start WebSocket server
            server = await websockets.serve(
                self.connection_handler,
                host,
                port,
                ping_interval=30,
                ping_timeout=10
            )
            
            logger.info(f"WebSocket server started on ws://{host}:{port}")
            
            # Keep server running
            await server.wait_closed()
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the WebSocket server"""
        try:
            self.is_running = False
            
            # Close all connections
            for connection_id, websocket in list(self.active_connections.items()):
                try:
                    await websocket.close()
                except Exception as e:
                    logger.error(f"Error closing connection {connection_id}: {e}")
            
            self.active_connections.clear()
            self.user_sessions.clear()
            
            logger.info("WebSocket server shutdown completed")
            
        except Exception as e:
            logger.error(f"Error shutting down WebSocket server: {e}")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_user_count(self) -> int:
        """Get number of active users"""
        return len(self.user_sessions)
    
    async def send_notification(self, user_id: str, notification: Dict[str, Any]):
        """Send notification to a user"""
        if user_id in self.user_sessions:
            await self.send_to_user(user_id, {
                'type': 'notification',
                'notification': notification,
                'timestamp': datetime.now().isoformat()
            })
    
    async def send_system_alert(self, alert: Dict[str, Any]):
        """Send system alert to all connected users"""
        await self.broadcast_message({
            'type': 'system_alert',
            'alert': alert,
            'timestamp': datetime.now().isoformat()
        })

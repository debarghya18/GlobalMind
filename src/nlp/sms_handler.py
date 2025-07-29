"""
SMS Fallback Module for GlobalMind
Provides SMS-based interaction capability
"""

import os
from typing import Optional
from twilio.rest import Client
from loguru import logger

from ..core.config import SMSConfig
from ..core.exceptions import SMSServiceError


class SMSHandler:
    """Handles SMS communications for the therapy assistant"""
    
    def __init__(self, config: SMSConfig):
        """
        Initialize SMS handler
        
        Args:
            config: Configuration for SMS service
        """
        self.config = config
        self.client = None
        
        # Initialize SMS client
        self._initialize_client()
        
        logger.info("SMS handler initialized")
    
    def _initialize_client(self):
        """Initialize Twilio SMS client"""
        try:
            # Create Twilio client
            self.client = Client(self.config.account_sid, self.config.auth_token)
            logger.info("Twilio client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize SMS client: {e}")
            self.client = None
            raise SMSServiceError(f"SMS client initialization failed: {e}", "SMS_001")
    
    def send_sms(self, to: str, message: str) -> bool:
        """
        Send an SMS message
        
        Args:
            to: Recipient phone number
            message: Message content
            
        Returns:
            bool: True if sent successfully
        """
        try:
            if not self.client:
                raise SMSServiceError("SMS client not available", "SMS_002")
            
            # Send SMS
            self.client.messages.create(
                body=message,
                from_=self.config.from_number,
                to=to
            )
            
            logger.info(f"SMS sent to {to}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return False
    
    def receive_sms(self):
        """
        Simulated SMS receiving (real implementation requires server-side handling)
        """
        pass
    
    def get_sms_statistics(self) -> dict:
        """
        Get SMS usage statistics
        
        Returns:
            dict: SMS statistics
        """
        return {
            'total_sent': 0,  # Placeholder for real stats
            'total_received': 0  # Placeholder for real stats
        }
    
    def cleanup(self):
        """Cleanup SMS handler resources"""
        logger.info("SMS handler cleanup completed")
    
    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            bool: True if valid
        """
        # Simple validation check (can be extended)
        if len(phone_number) < 10 or not phone_number.isdigit():
            logger.warning(f"Invalid phone number: {phone_number}")
            return False
        return True


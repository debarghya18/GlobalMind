"""
Encryption manager for GlobalMind
Handles end-to-end encryption and key management
"""

import os
import hashlib
import secrets
from typing import Dict, Any, Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from loguru import logger
import base64
import json
from datetime import datetime, timedelta

from ..core.exceptions import SecurityError
from ..core.config import SecurityConfig


class EncryptionManager:
    """Manages encryption and decryption operations"""
    
    def __init__(self, config: SecurityConfig):
        """
        Initialize encryption manager
        
        Args:
            config: Security configuration
        """
        self.config = config
        self.master_key: Optional[bytes] = None
        self.fernet: Optional[Fernet] = None
        self.key_rotation_interval = timedelta(days=config.key_rotation_days)
        self.last_key_rotation = datetime.now()
        
        # Initialize encryption
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize encryption keys and cipher"""
        try:
            # Generate or load master key
            self.master_key = self._get_or_create_master_key()
            
            # Initialize Fernet cipher
            self.fernet = Fernet(self.master_key)
            
            logger.info("Encryption initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            raise SecurityError(f"Encryption initialization failed: {e}", "SEC_001")
    
    def _get_or_create_master_key(self) -> bytes:
        """Get existing master key or create new one"""
        key_file = "data/master.key"
        
        try:
            # Try to load existing key
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            
            # Create new key
            logger.info("Creating new master encryption key")
            key = Fernet.generate_key()
            
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            # Save key securely
            with open(key_file, 'wb') as f:
                f.write(key)
            
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
            
            return key
            
        except Exception as e:
            logger.error(f"Failed to handle master key: {e}")
            raise SecurityError(f"Master key handling failed: {e}", "SEC_001")
    
    def encrypt_data(self, data: Union[str, bytes, Dict[str, Any]]) -> str:
        """
        Encrypt data using AES-256-GCM
        
        Args:
            data: Data to encrypt
            
        Returns:
            str: Base64 encoded encrypted data
        """
        try:
            # Convert data to bytes if needed
            if isinstance(data, dict):
                data = json.dumps(data)
            
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Encrypt data
            encrypted_data = self.fernet.encrypt(data)
            
            # Return base64 encoded string
            return base64.b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Data encryption failed: {e}")
            raise SecurityError(f"Data encryption failed: {e}", "SEC_002")
    
    def decrypt_data(self, encrypted_data: str) -> bytes:
        """
        Decrypt data
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            bytes: Decrypted data
        """
        try:
            # Decode base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Decrypt data
            decrypted_data = self.fernet.decrypt(encrypted_bytes)
            
            return decrypted_data
            
        except Exception as e:
            logger.error(f"Data decryption failed: {e}")
            raise SecurityError(f"Data decryption failed: {e}", "SEC_002")
    
    def encrypt_json(self, data: Dict[str, Any]) -> str:
        """
        Encrypt JSON data
        
        Args:
            data: Dictionary to encrypt
            
        Returns:
            str: Encrypted JSON string
        """
        return self.encrypt_data(json.dumps(data))
    
    def decrypt_json(self, encrypted_data: str) -> Dict[str, Any]:
        """
        Decrypt JSON data
        
        Args:
            encrypted_data: Encrypted JSON string
            
        Returns:
            Dict[str, Any]: Decrypted dictionary
        """
        try:
            decrypted_bytes = self.decrypt_data(encrypted_data)
            return json.loads(decrypted_bytes.decode('utf-8'))
        except Exception as e:
            logger.error(f"JSON decryption failed: {e}")
            raise SecurityError(f"JSON decryption failed: {e}", "SEC_002")
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
        """
        Hash password with salt
        
        Args:
            password: Password to hash
            salt: Optional salt (will be generated if not provided)
            
        Returns:
            tuple: (hashed_password, salt)
        """
        try:
            if salt is None:
                salt = secrets.token_bytes(32)
            
            # Use PBKDF2 with SHA-256
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            password_bytes = password.encode('utf-8')
            hashed_password = kdf.derive(password_bytes)
            
            return (
                base64.b64encode(hashed_password).decode('utf-8'),
                base64.b64encode(salt).decode('utf-8')
            )
            
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise SecurityError(f"Password hashing failed: {e}", "SEC_002")
    
    def anonymize_user_id(self, original_id: str) -> str:
        """
        Create anonymous user ID from original ID
        
        Args:
            original_id: Original user identifier
            
        Returns:
            str: Anonymous user ID
        """
        try:
            # Create a hash of the original ID for anonymization
            hash_bytes = hashlib.sha256(original_id.encode('utf-8')).digest()
            
            # Convert to base64 for storage
            anonymous_id = base64.b64encode(hash_bytes).decode('utf-8')
            
            # Add a prefix to identify as anonymous
            return f"anon_{anonymous_id[:16]}"
            
        except Exception as e:
            logger.error(f"User ID anonymization failed: {e}")
            raise SecurityError(f"User ID anonymization failed: {e}", "SEC_002")
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Password to verify
            hashed_password: Stored hash
            salt: Stored salt
            
        Returns:
            bool: True if password matches
        """
        try:
            # Hash the provided password with the stored salt
            computed_hash, _ = self.hash_password(
                password, 
                base64.b64decode(salt.encode('utf-8'))
            )
            
            # Compare hashes
            return computed_hash == hashed_password
            
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    def generate_session_token(self) -> str:
        """
        Generate secure session token
        
        Returns:
            str: Session token
        """
        try:
            # Generate random token
            token = secrets.token_urlsafe(32)
            
            # Add timestamp
            timestamp = datetime.now().isoformat()
            
            # Create token data
            token_data = {
                'token': token,
                'timestamp': timestamp,
                'expires': (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            # Encrypt token data
            encrypted_token = self.encrypt_json(token_data)
            
            return encrypted_token
            
        except Exception as e:
            logger.error(f"Session token generation failed: {e}")
            raise SecurityError(f"Session token generation failed: {e}", "SEC_002")
    
    def validate_session_token(self, encrypted_token: str) -> bool:
        """
        Validate session token
        
        Args:
            encrypted_token: Encrypted session token
            
        Returns:
            bool: True if token is valid
        """
        try:
            # Decrypt token
            token_data = self.decrypt_json(encrypted_token)
            
            # Check expiration
            expires = datetime.fromisoformat(token_data['expires'])
            if datetime.now() > expires:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Session token validation failed: {e}")
            return False
    
    def rotate_keys(self):
        """Rotate encryption keys"""
        try:
            # Check if rotation is needed
            if datetime.now() - self.last_key_rotation < self.key_rotation_interval:
                return
            
            logger.info("Starting key rotation")
            
            # Generate new master key
            new_key = Fernet.generate_key()
            
            # Save old key for decryption of existing data
            old_key_file = f"data/master.key.{self.last_key_rotation.strftime('%Y%m%d')}"
            os.rename("data/master.key", old_key_file)
            
            # Save new key
            with open("data/master.key", 'wb') as f:
                f.write(new_key)
            
            # Update encryption
            self.master_key = new_key
            self.fernet = Fernet(new_key)
            self.last_key_rotation = datetime.now()
            
            logger.info("Key rotation completed successfully")
            
        except Exception as e:
            logger.error(f"Key rotation failed: {e}")
            raise SecurityError(f"Key rotation failed: {e}", "SEC_001")
    
    def cleanup(self):
        """Clean up sensitive data from memory"""
        try:
            # Clear master key
            if self.master_key:
                self.master_key = None
            
            # Clear Fernet instance
            if self.fernet:
                self.fernet = None
            
            logger.info("Encryption cleanup completed")
            
        except Exception as e:
            logger.error(f"Encryption cleanup failed: {e}")
    
    def get_encryption_status(self) -> Dict[str, Any]:
        """Get encryption status"""
        return {
            'algorithm': self.config.encryption_algorithm,
            'key_rotation_days': self.config.key_rotation_days,
            'last_rotation': self.last_key_rotation.isoformat(),
            'next_rotation': (self.last_key_rotation + self.key_rotation_interval).isoformat(),
            'encryption_active': self.fernet is not None
        }

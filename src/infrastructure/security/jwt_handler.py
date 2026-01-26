"""JWT Token Handler."""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt

from src.config import get_settings

settings = get_settings()


class JWTHandler:
    """
    JWT token creation and validation.
    """
    
    def __init__(self) -> None:
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expires = settings.JWT_ACCESS_TOKEN_EXPIRES
        self.refresh_token_expires = settings.JWT_REFRESH_TOKEN_EXPIRES
    
    def create_access_token(
        self, 
        subject: str, 
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create an access token."""
        expires_delta = timedelta(seconds=self.access_token_expires)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
        }
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, subject: str) -> str:
        """Create a refresh token."""
        expires_delta = timedelta(seconds=self.refresh_token_expires)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a token."""
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")
    
    def get_subject(self, token: str) -> str:
        """Extract subject from token."""
        payload = self.decode_token(token)
        return payload.get("sub")

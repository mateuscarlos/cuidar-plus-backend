"""Password Hashing Utility."""
import bcrypt


class PasswordHasher:
    """
    Password hashing and verification using bcrypt.
    """
    
    def hash(self, password: str) -> str:
        """Hash a plain password."""
        # Bcrypt has a 72 byte limit
        password_bytes = password[:72].encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hash."""
        password_bytes = plain_password[:72].encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)


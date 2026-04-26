from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

# Password hashing configuration (bcrypt is industry standard)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    """
    Generate a JWT access token.

    Adds an expiration claim (`exp`) to the payload and signs the token
    using the application's secret key and algorithm.

    Args:
        data (dict): Payload data to encode (e.g., user ID, email, role)

    Returns:
        str: Signed JWT token
    """

    # Copy payload to avoid mutating the original input
    to_encode = data.copy()

    # Set token expiration based on configured duration
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    # Encode and sign the JWT
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def hash_password(password: str):
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Verify a plaintext password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

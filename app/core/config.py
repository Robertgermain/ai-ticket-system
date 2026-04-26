from dotenv import load_dotenv
import os

# Load environment variables from .env file into the system environment
load_dotenv()


class Settings:
    """
    Application configuration loaded from environment variables.

    This centralizes access to sensitive values such as:
    - JWT authentication settings
    - API keys (e.g., OpenAI)
    - Token expiration configuration
    """

    # Secret key used for signing JWT tokens
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # Algorithm used for JWT encoding/decoding
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    # Access token expiration time (in minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # OpenAI API key used for AI ticket classification
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


# Singleton instance used throughout the application
settings = Settings()

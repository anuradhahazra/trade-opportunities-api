import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY: str = os.getenv("API_KEY", "dev-api-key-12345")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60  # seconds
    SESSION_TIMEOUT: int = 3600  # seconds

settings = Settings()


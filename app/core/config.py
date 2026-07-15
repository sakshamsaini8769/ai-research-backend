import os
from pathlib import Path
from dotenv import load_dotenv

# Backend root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env file
load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Application Settings
    """

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY", "")

    API_TITLE = "AI Research Assistant API"
    API_VERSION = "2.0.0"


settings = Settings()

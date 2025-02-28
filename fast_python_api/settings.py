import os
import dotenv
from pydantic import Field
from typing import Any, Dict
from pydantic_settings import BaseSettings


dotenv.load_dotenv()


class Settings(BaseSettings):
    """
    Settings for FastAPI application.

    All settings are loaded from environment variables.
    Settings are grouped into categories. Each category has its own class.
    """
    env_file: str = os.path.join(os.path.dirname(__file__), '.env')
    env_file_encoding: str = 'utf-8'
    test_service_url: str = "https://randomuser.me/api"
    param_test_api: Dict[str, Any] = Field(
        default_factory=lambda: {"results": "5"}
    )
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db" # noqa C901
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_VERSION: str = "1.0.0"


settings = Settings()

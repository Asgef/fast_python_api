from typing import Any, Dict
import dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
import os


dotenv.load_dotenv()


class Settings(BaseSettings):
    env_file: str = os.path.join(os.path.dirname(__file__), '.env')
    env_file_encoding: str = 'utf-8'
    test_service_url: str = "https://randomuser.me/api"
    param_test_api: Dict[str, Any] = Field(
        default_factory=lambda: {"results": "5"}
    )
    DEBUG: bool = Field(default=False)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
        json_schema_extra={'env': 'DATABASE_URL'}
    )
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    SECRET_KEY: str = Field(
        json_schema_extra={'env': 'SECRET_KEY'}
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_VERSION: str = "1.0.0"


settings = Settings()

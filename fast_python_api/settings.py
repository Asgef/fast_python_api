from typing import Any, Dict
import dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
import os


dotenv.load_dotenv()


class Settings(BaseSettings):
    test_service_url: str
    param_test_api: Dict[str, Any] = Field(
        default_factory=lambda: {"results": "5"}
    )
    DEBUG: bool = Field(default=False)
    DATABASE_URL: str

    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings(
    _env_file=os.path.join(os.path.dirname(__file__), '.env')
)

from typing import Any, Dict
import dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
import os


dotenv.load_dotenv()


class Settings(BaseSettings):
    test_service_url: str = Field(
        ..., json_schema_extra={'env': 'TEST_SERVICE_URL'}
    )
    param_test_api: Dict[str, Any] = Field(
        default_factory=lambda: {"results": "5"}
    )
    DEBUG: bool = Field(default=False)
    database_url: str = Field(
        default="sqlite:///test.db",
        json_schema_extra={'env': 'DATABASE_URL'}
    )

    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings(
    _env_file=os.path.join(os.path.dirname(__file__), '.env')
)

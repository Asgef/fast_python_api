from typing import Any, Dict
import dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


dotenv.load_dotenv()


class Settings(BaseSettings):
    test_service_url: str
    param_test_api: Dict[str, Any] = Field(
        default_factory=lambda: {"results": "5"}
    )
    DEBUG: bool = Field(default=False, env='DEBUG')
    DATABASE_URL: str = Field(..., env='DATABASE_URL')

    model_config = ConfigDict(env_file='../.env', extra='ignore')


settings = Settings()

from typing import Any, Dict
import dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


dotenv.load_dotenv()


PARAM_TEST_API = {'results': 5, 'inc': 'name,email'}


class Settings(BaseSettings):
    test_service_url: str
    param_test_api: Dict[str, Any] = Field(
        default_factory=lambda: {"results": "5", "inc": "name,email"}
    )

    class Config:
        env_file = '../.env'
        extra = 'ignore'


settings = Settings()

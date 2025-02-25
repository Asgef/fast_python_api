from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional


class RandomUserParams(BaseModel):
    results: int = Field(
        default=5,
        ge=1,
        le=20,
        title="results",
        description="Number of users to return",
    )
    gender: Optional[Literal["male", "female"]] = Field(
        default=None,
        title="gender",
        description="Gender of the users",
    )
    nat: Optional[str] = Field(
        default=None,
        title="nat",
        description="Nationality of the users",
    )

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "results": 10,
            "gender": "female"
        }
    })

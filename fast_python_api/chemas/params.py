from pydantic import BaseModel, Field
from typing import Literal, Optional


class RandomUserParams(BaseModel):
    results: int = Field(
        default=5,
        ge=1,
        le=20,
        title="Number of users to return",
        description="Number of users to return",
        json_schema_extra={"example": 10},
    )
    gender: Optional[Literal["male", "female"]] = Field(
        default=None,
        title="Gender of the users",
        description="Gender of the users",
        json_schema_extra={"example": "female"},
    )
    nat: Optional[str] = Field(
        default=None,
        title="Nationality of the users",
        description="Nationality of the users",
        json_schema_extra={"example": "GB"},
    )

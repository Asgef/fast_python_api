from pydantic import BaseModel, Field
from typing import Literal, Optional


class RandomUserParams(BaseModel):
    results: int = Field(
        default=5,
        ge=1,
        le=20,
        title="Number of users",
        description="Number of users to return",
    )
    gender: Optional[Literal["male", "female"]] = Field(
        default=None,
        title="Gender",
        description="Gender of the users",
    )
    nat: Optional[str] = Field(
        default=None,
        title="Nationality",
        description="Nationality of the users",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "results": 10,
                "gender": "male",
                "nat": "US"
            }
        }

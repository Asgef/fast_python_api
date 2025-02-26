from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.fields import Field


class Token(BaseModel):
    """
    Access token
    """
    access_token: str = Field(
        ..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaGFuIjoiMjMwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"} # noqa C901
    )
    token_type: str = Field(..., json_schema_extra={"example": "bearer"})


class TokenData(BaseModel):
    """
    Data of User
    """
    username: str | None = Field(None, json_schema_extra={"example": "johndoe"})
    role: str | None = Field(None, json_schema_extra={"example": "user"})
    id: str | None = Field(
        None,
        json_schema_extra={"example": "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a"}
    )

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johndoe",
            "role": "user",
            "id": "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a"
        }
    })

from pydantic import BaseModel
import uuid


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None
    id: str | None = None


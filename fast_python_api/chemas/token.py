from pydantic import BaseModel


class Token(BaseModel):
    """
    Access token
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Data of User
    """
    username: str | None = None
    role: str | None = None
    id: str | None = None

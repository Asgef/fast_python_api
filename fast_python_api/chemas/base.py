from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime
import uuid


class NameBase(BaseModel):
    title: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class LoginBase(BaseModel):
    username: str
    uuid: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    id: str
    name: NameBase
    login: LoginBase
    dob: date
    city: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

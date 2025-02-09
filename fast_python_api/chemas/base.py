from pydantic import BaseModel, EmailStr
from datetime import date, datetime
import uuid


class NameBase(BaseModel):
    title: str
    first_name: str
    last_name: str

    class Config:
        model_config = {'from_attributes': True}


class LoginBase(BaseModel):
    username: str
    uuid: uuid.UUID

    class Config:
        model_config = {'from_attributes': True}


class UserBase(BaseModel):
    id: str
    name: NameBase
    login: LoginBase
    dob: date
    city: str
    email: EmailStr
    created_at: datetime

    class Config:
        model_config = {'from_attributes': True}

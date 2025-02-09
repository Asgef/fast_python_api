from fast_python_api.chemas.base import UserBase, LoginBase


class LoginInDB(LoginBase):
    password: str

    class Config:
        model_config = {'from_attributes': True}


class UserInDB(UserBase):
    login: LoginInDB

    class Config:
        model_config = {'from_attributes': True}

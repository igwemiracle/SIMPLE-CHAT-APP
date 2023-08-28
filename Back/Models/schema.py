from pydantic import BaseModel
from typing import Optional


class UserValidate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


# class Admin():
#     is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str

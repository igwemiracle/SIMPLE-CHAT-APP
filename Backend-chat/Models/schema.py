from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union


class UserValidate(BaseModel):
    username: str
    password: Union[str, int] = None
    email: Optional[str] = None


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    sender: str
    recipient: str


class Messages(MessageBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        form_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

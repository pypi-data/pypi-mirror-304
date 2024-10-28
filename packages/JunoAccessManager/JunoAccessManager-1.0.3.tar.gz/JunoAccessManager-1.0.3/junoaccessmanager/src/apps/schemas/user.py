from pydantic import BaseModel
from junoaccessmanager.src.apps.models.user import UserStatusEnum
from typing import Union


class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    phone: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    status: UserStatusEnum
    mq_token: str

    class Config:
        from_attributes = True

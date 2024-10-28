import enum

from sqlalchemy import Column, Enum, String, Text

from junoaccessmanager.src.common.models import BaseModel


class UserStatusEnum(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(BaseModel):
    __tablename__ = "user"

    username = Column(String(64), unique=True, nullable=False)
    hashed_password = Column(String(64), nullable=False)
    email = Column(String(64), unique=True)
    phone = Column(String(64), unique=True)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.INACTIVE, nullable=False)
    mq_token = Column(Text, nullable=False)

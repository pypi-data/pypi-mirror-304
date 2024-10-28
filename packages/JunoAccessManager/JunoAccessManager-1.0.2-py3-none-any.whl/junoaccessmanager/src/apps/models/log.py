from sqlalchemy import Column, ForeignKey, Integer, Text
from junoaccessmanager.src.common.models import BaseModel


class Log(BaseModel):
    __tablename__ = "log"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)

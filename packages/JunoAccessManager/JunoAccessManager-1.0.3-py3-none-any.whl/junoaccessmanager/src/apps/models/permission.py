import enum
from junoaccessmanager.src.common.models import BaseModel
from sqlalchemy import Column, BOOLEAN, Enum, String, ForeignKey, UniqueConstraint


class TopicActions(enum.Enum):
    PRODUCE = 'produce'
    CONSUME = 'consume'
    BOTH = 'produce_consume'


class Permission(BaseModel):
    __tablename__ = "permission"

    username = Column(String(64), ForeignKey("user.username"), nullable=False)
    tenant = Column(String(64), nullable=False)
    namespace = Column(String(64), nullable=False)
    topic = Column(String(64), nullable=False)
    action = Column(Enum(TopicActions), nullable=False)

    __table_args__ = (UniqueConstraint('username', 'tenant', 'namespace', 'topic', name='unique_permission'),)

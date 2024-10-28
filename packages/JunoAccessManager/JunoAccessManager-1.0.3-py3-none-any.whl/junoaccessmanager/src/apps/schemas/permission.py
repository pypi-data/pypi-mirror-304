from pydantic import BaseModel
from junoaccessmanager.src.apps.models.permission import TopicActions


class PermissionBase(BaseModel):
    username: str
    tenant: str
    namespace: str
    topic: str


class PermissionCreate(PermissionBase):
    action: TopicActions


class Permission(PermissionBase):
    id: int
    action: TopicActions

    class Config:
        from_attributes = True


# class Permissions(Permission):
#     index: int = 0

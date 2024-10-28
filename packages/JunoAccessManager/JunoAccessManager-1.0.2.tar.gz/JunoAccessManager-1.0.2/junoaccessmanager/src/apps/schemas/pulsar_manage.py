from typing import List
from pydantic import BaseModel
from jam.src.apps.models.permission import TopicActions


class Tenant(BaseModel):
    tenant: str


class TenantCreate(Tenant):
    clusters: List[str]


class Namespace(Tenant):
    namespace: str


class Topic(Namespace):
    topic: str


class Subscription(Topic):
    subscription: str


class NamespaceRole(Namespace):
    role: str


class NamespaceRoleCreate(NamespaceRole):
    actions: TopicActions


class TopicRole(Topic):
    role: str


class TopicRoleCreate(TopicRole):
    actions: TopicActions

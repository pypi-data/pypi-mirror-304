from enum import Enum
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from junoaccessmanager.src.apps.schemas.user import User
from junoaccessmanager.src.apps.schemas.pulsar_manage import (
    Tenant,
    TenantCreate,
    Namespace,
    Topic,
    Subscription,
    NamespaceRole,
    NamespaceRoleCreate,
    TopicRole,
    TopicRoleCreate
)
from junoaccessmanager.src.apps.controllers.pulsar_manage import (
    get_brokers,
    get_clusters,
    get_tenants,
    get_namespaces,
    get_topics,
    get_roles_in_namespace,
    get_roles_in_topic,
    create_tenant,
    delete_tenant,
    create_namespace,
    delete_namespace,
    create_topic,
    delete_topic,
    create_subscription,
    delete_subscription,
    grant_namespace_permission,
    delete_namespace_permission,
    grant_topic_permission,
    delete_topic_permission,
)
from junoaccessmanager.src.common.dependencies.authorization import get_admin_user
from junoaccessmanager.src.common.dependencies.database import get_mysql_db
from junoaccessmanager.src.common.response import R

pulsar_router = APIRouter()


class QueryBy(Enum):
    BROKERS = 'brokers'
    CLUSTERS = 'clusters'
    TENANTS = 'tenants'


@pulsar_router.get("/admin/query", summary='【管理员】根据指定范围，查询各自在Pulsar上拥有的下级')
async def read_tenants(
    query_by: QueryBy,
    current_user: User = Depends(get_admin_user)
):
    if query_by == QueryBy.BROKERS:
        resp = get_brokers()
    elif query_by == QueryBy.CLUSTERS:
        resp = get_clusters()
    else:
        resp = get_tenants()

    if resp.status_code == 200:
        return R.ok(user_id=current_user.id, msg='读取所有信息成功', data=resp.json())
    else:
        return R.err(user_id=current_user.id, msg='读取所有信息失败')


@pulsar_router.get("/admin/namespaces/{tenant}", summary='【管理员】查询Pulsar在指定Tenant下拥有的Namespace')
async def read_namespaces(
    tenant: str,
    current_user: User = Depends(get_admin_user)
):
    resp = get_namespaces(tenant=tenant)

    if resp.status_code == 200:
        return R.ok(user_id=current_user.id, msg=f'读取{tenant}/下的所有namespaces成功', data=resp.json())
    else:
        return R.err(user_id=current_user.id, msg=f'读取{tenant}/下的所有namespaces失败')


@pulsar_router.get("/admin/topics/{tenant}/{namespace}", summary='【管理员】查询Pulsar在指定Namespace下拥有的Topic')
async def read_topics(
    tenant: str,
    namespace: str,
    current_user: User = Depends(get_admin_user)
):
    resp = get_topics(tenant=tenant, namespace=namespace)

    if resp.status_code == 200:
        return R.ok(user_id=current_user.id, msg=f'读取{tenant}/{namespace}下的所有topics成功', data=resp.json())
    else:
        return R.err(user_id=current_user.id, msg=f'读取{tenant}/{namespace}下的所有topics失败')


@pulsar_router.get("/admin/roles/{tenant}/{namespace}", summary='【管理员】查询Pulsar在指定Namespace下拥有的子集')
async def read_roles_in_namespace(
    tenant: str,
    namespace: str,
    current_user: User = Depends(get_admin_user)
):
    resp = get_roles_in_namespace(tenant=tenant, namespace=namespace)

    if resp.status_code == 200:
        return R.ok(user_id=current_user.id, msg=f'读取{tenant}/{namespace}下的所有roles成功', data=resp.json())
    else:
        return R.err(user_id=current_user.id, msg=f'读取{tenant}/{namespace}下的所有roles失败')


@pulsar_router.get("/admin/roles/{tenant}/{namespace}/{topic}", summary='【管理员】查询Pulsar在指定Topic下允许的权限用户')
async def read_roles_in_topic(
    tenant: str,
    namespace: str,
    topic: str,
    current_user: User = Depends(get_admin_user)
):
    resp = get_roles_in_topic(tenant=tenant, namespace=namespace, topic=topic)

    if resp.status_code == 200:
        return R.ok(user_id=current_user.id, msg=f'读取{tenant}/{namespace}/{topic}下的所有roles成功', data=resp.json())
    else:
        return R.err(user_id=current_user.id, msg=f'读取{tenant}/{namespace}/{topic}下的所有roles失败')


@pulsar_router.post("/admin/tenant", summary='【管理员】在Pulsar上创建指定名称的Tenant')
async def add_tenant(
    add_tenant_param: TenantCreate,
    current_user: User = Depends(get_admin_user)
):
    resp = create_tenant(
        clusters=add_tenant_param.clusters,
        tenant=add_tenant_param.tenant
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'创建{add_tenant_param.tenant}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'创建{add_tenant_param.tenant}失败')


@pulsar_router.delete("/admin/tenant", summary='【管理员】在Pulsar上删除指定名称的Tenant')
async def subtract_tenant(
    subtract_tenant_param: Tenant,
    current_user: User = Depends(get_admin_user)
):
    resp = delete_tenant(tenant=subtract_tenant_param.tenant)

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'删除{subtract_tenant_param.tenant}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'删除{subtract_tenant_param.tenant}失败')


@pulsar_router.post("/admin/namespace", summary='【管理员】在Pulsar上创建指定名称的Namespace')
async def add_namespace(
    add_namespace_param: Namespace,
    current_user: User = Depends(get_admin_user)
):
    resp = create_namespace(
        tenant=add_namespace_param.tenant,
        namespace=add_namespace_param.namespace
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'创建{add_namespace_param.namespace}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'创建{add_namespace_param.namespace}失败')


@pulsar_router.delete("/admin/namespace", summary='【管理员】在Pulsar上删除指定名称的Namespace')
async def subtract_namespace(
    subtract_namespace_param: Namespace,
    current_user: User = Depends(get_admin_user)
):
    resp = delete_namespace(
        tenant=subtract_namespace_param.tenant,
        namespace=subtract_namespace_param.namespace
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'删除{subtract_namespace_param.namespace}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'删除{subtract_namespace_param.namespace}失败')


@pulsar_router.post("/admin/topic", summary='【管理员】在Pulsar上创建指定名称的Topic')
async def add_topic(
    add_topic_param: Topic,
    current_user: User = Depends(get_admin_user)
):
    resp = create_topic(
        tenant=add_topic_param.tenant,
        namespace=add_topic_param.namespace,
        topic=add_topic_param.topic
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'创建{add_topic_param.topic}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'创建{add_topic_param.topic}失败')


@pulsar_router.delete("/admin/topic", summary='【管理员】在Pulsar上删除指定名称的Topic')
async def subtract_topic(
    subtract_topic_param: Topic,
    current_user: User = Depends(get_admin_user)
):
    resp = delete_topic(
        tenant=subtract_topic_param.tenant,
        namespace=subtract_topic_param.namespace,
        topic=subtract_topic_param.topic
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'删除{subtract_topic_param.topic}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'删除{subtract_topic_param.topic}失败')


@pulsar_router.post("/admin/subscription", summary='【管理员】在Pulsar上创建指定名称的Subscription')
async def add_subscription(
    add_subscription_param: Subscription,
    current_user: User = Depends(get_admin_user)
):
    resp = create_subscription(
        tenant=add_subscription_param.tenant,
        namespace=add_subscription_param.namespace,
        topic=add_subscription_param.topic,
        subscription=add_subscription_param.subscription
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'创建{add_subscription_param.subscription}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'创建{add_subscription_param.subscription}失败')


@pulsar_router.delete("/admin/subscription", summary='【管理员】在Pulsar上删除指定名称的Subscription')
async def subtract_subscription(
    subtract_subscription_param: Subscription,
    current_user: User = Depends(get_admin_user)
):
    resp = delete_subscription(
        tenant=subtract_subscription_param.tenant,
        namespace=subtract_subscription_param.namespace,
        topic=subtract_subscription_param.topic,
        subscription=subtract_subscription_param.subscription
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'删除{subtract_subscription_param.subscription}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'删除{subtract_subscription_param.subscription}失败')


@pulsar_router.post("/admin/permission/namespace", summary='【管理员】在Pulsar上的指定Namespace中对指定用户创建指定权限')
async def add_permission_in_namespace(
    add_role_param: NamespaceRoleCreate,
    current_user: User = Depends(get_admin_user)
):
    resp = grant_namespace_permission(
        tenant=add_role_param.tenant,
        namespace=add_role_param.namespace,
        role=add_role_param.role,
        actions=add_role_param.actions
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'创建{add_role_param.role}的{add_role_param.actions}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'创建{add_role_param.role}的{add_role_param.actions}失败')


@pulsar_router.delete("/admin/permission/namespace", summary='【管理员】在Pulsar上的指定Namespace中删除指定用户的权限')
async def subtract_permission_in_namespace(
    subtract_role_param: NamespaceRole,
    current_user: User = Depends(get_admin_user)
):
    resp = delete_namespace_permission(
        tenant=subtract_role_param.tenant,
        namespace=subtract_role_param.namespace,
        role=subtract_role_param.role
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'删除{subtract_role_param.role}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'删除{subtract_role_param.role}失败')


@pulsar_router.post("/admin/permission/topic", summary='【管理员】在Pulsar上的指定Topic中对指定用户创建指定权限')
async def add_permission_in_topic(
    add_role_param: TopicRoleCreate,
    current_user: User = Depends(get_admin_user)
):
    resp = grant_topic_permission(
        tenant=add_role_param.tenant,
        namespace=add_role_param.namespace,
        topic=add_role_param.topic,
        role=add_role_param.role,
        actions=add_role_param.actions
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'创建{add_role_param.role}的{add_role_param.actions}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'创建{add_role_param.role}的{add_role_param.actions}失败')


@pulsar_router.delete("/admin/permission/topic", summary='【管理员】在Pulsar上的指定Topic中删除指定用户的权限')
async def subtract_permission_in_topic(
    subtract_role_param: TopicRole,
    current_user: User = Depends(get_admin_user)
):
    resp = delete_topic_permission(
        tenant=subtract_role_param.tenant,
        namespace=subtract_role_param.namespace,
        topic=subtract_role_param.topic,
        role=subtract_role_param.role
    )

    if resp.status_code == 204:
        return R.ok(user_id=current_user.id, msg=f'删除{subtract_role_param.role}成功')
    else:
        return R.err(user_id=current_user.id, msg=f'删除{subtract_role_param.role}失败')

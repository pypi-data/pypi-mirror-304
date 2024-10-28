from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from enum import Enum

from junoaccessmanager.src.apps.models.permission import TopicActions
from junoaccessmanager.src.apps.schemas.permission import PermissionBase, PermissionCreate
from junoaccessmanager.src.apps.schemas.user import User
from junoaccessmanager.src.apps.services.user import get_user_by_username
from junoaccessmanager.src.apps.services.permission import (
    create_permission,
    update_permission,
    delete_permission,
    get_all_permissions,
    get_permission_by_id,
    get_permission_by_username,
    get_permission_by_tenant,
    get_permission_by_namespace,
    get_permission_by_topic,
    get_permission_by_action,
    get_permission_by_user_tenant_namespace,
    get_permission_by_user_tenant_namespace_topic
)
from junoaccessmanager.src.apps.controllers.pulsar_manage import (
    create_mq_token,
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
from junoaccessmanager.src.common.dependencies.authorization import get_current_active_user, get_admin_user
from junoaccessmanager.src.common.dependencies.database import get_mysql_db
from junoaccessmanager.src.common.response import R

permission_router = APIRouter()


@permission_router.post("/admin/add", summary='【管理员】为指定用户添加对指定Topic的读/写权限')
async def create(
    action: TopicActions,
    permission_base: PermissionBase,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_mysql_db)
):
    user = get_user_by_username(db=db, username=permission_base.username)
    if not user:
        return R.err(user_id=-1, msg='查无此人')

    db_permission = get_permission_by_user_tenant_namespace_topic(db=db, permission_base=permission_base)
    if not db_permission:
        resp = grant_topic_permission(
            tenant=permission_base.tenant,
            namespace=permission_base.namespace,
            topic=permission_base.topic,
            role=permission_base.username,
            actions=action
        )
        if resp.status_code != 204:
            return R.err(user_id=current_user.id, msg='Pulsar添加权限失败')

        permission_create = PermissionCreate(
            username=permission_base.username,
            tenant=permission_base.tenant,
            namespace=permission_base.namespace,
            topic=permission_base.topic,
            action=action
        )
        resp = create_permission(db=db, permission_create=permission_create)
    elif db_permission.action == TopicActions.BOTH or db_permission.action == action:
        return R.err(user_id=current_user.id, msg='添加权限失败，权限已存在')
    else:
        resp = grant_topic_permission(
            tenant=permission_base.tenant,
            namespace=permission_base.namespace,
            topic=permission_base.topic,
            role=permission_base.username,
            actions=TopicActions.BOTH
        )
        if resp.status_code != 204:
            return R.err(user_id=current_user.id, msg='Pulsar添加权限失败')

        resp = update_permission(db=db, action=TopicActions.BOTH, permission_base=permission_base)

    if resp:
        return R.ok(user_id=current_user.id, msg='添加权限成功')
    else:
        return R.err(user_id=current_user.id, msg='添加权限失败')


@permission_router.delete("/admin/delete", summary='【管理员】从指定Topic中删除对指定用户的所有访问权限')
async def delete(
    permission_delete: PermissionBase,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_mysql_db),
):
    user = get_user_by_username(db=db, username=permission_delete.username)
    if not user:
        return R.err(user_id=current_user.id, msg='查无此人')

    resp = delete_topic_permission(
        tenant=permission_delete.tenant,
        namespace=permission_delete.namespace,
        topic=permission_delete.topic,
        role=permission_delete.username
    )
    if resp.status_code != 204:
        return R.err(user_id=current_user.id, msg='Pulsar删除权限失败')

    resp = delete_permission(db=db, permission_base=permission_delete)

    if resp:
        return R.ok(user_id=current_user.id, msg='删除权限成功')
    else:
        return R.err(user_id=current_user.id, msg='Pulsar删除权限成功，DB删除权限失败')


class QueryBy(Enum):
    PERMISSION_ID = 'id'
    USERNAME = 'username'
    TENANT = 'tenant'
    NAMESPACE = 'namespace'
    TOPIC = 'topic'
    ACTION = 'action'
    ALL = 'all'


@permission_router.get("/admin/query", summary='【管理员】根据指定信息查询权限数据库')
async def read_permission(
    query_by: QueryBy,
    query_value: int | str | TopicActions | None = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_mysql_db),
):
    if query_by == QueryBy.PERMISSION_ID:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，缺少查询参数')
        db_permissions = [get_permission_by_id(db=db, permission_id=query_value)]
    elif query_by == QueryBy.USERNAME:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，缺少查询参数')
        db_permissions = get_permission_by_username(db=db, username=query_value)
    elif query_by == QueryBy.TENANT:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，缺少查询参数')
        db_permissions = get_permission_by_tenant(db=db, tenant=query_value)
    elif query_by == QueryBy.NAMESPACE:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，缺少查询参数')
        db_permissions = get_permission_by_namespace(db=db, namespace=query_value)
    elif query_by == QueryBy.TOPIC:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，缺少查询参数')
        db_permissions = get_permission_by_topic(db=db, topic=query_value)
    elif query_by == QueryBy.ACTION:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，缺少查询参数')
        if type(query_value) != str or query_value not in [member.value for member in TopicActions]:
            return R.err(user_id=current_user.id, msg=f'查询权限失败，请输入用于查找的动作字符【produce_consume/consume/produce】')
        db_permissions = get_permission_by_action(db=db, action=query_value)
    else:
        if query_value:
            return R.err(user_id=current_user.id, msg='查询权限失败，查询参数多余')
        db_permissions = get_all_permissions(db=db)

    if not db_permissions or not db_permissions[0]:
        return R.err(user_id=current_user.id, msg=f'查询权限失败，指定权限不存在')

    for permission in db_permissions:
        permission.index = db_permissions.index(permission)

    return R.ok(user_id=current_user.id, msg='查询权限成功', data=db_permissions)


@permission_router.get("/admin/{username}/{tenant}/{namespace}/{topic}", summary='【管理员】查询指定topic下的所有权限用户')
async def read_permission_by_user_tenant_namespace_topic(
    username: str,
    tenant: str,
    namespace: str,
    topic: str,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_mysql_db),
):
    permission_base = PermissionBase(
        username=username,
        tenant=tenant,
        namespace=namespace,
        topic=topic
    )
    db_permission = get_permission_by_user_tenant_namespace_topic(db=db, permission_base=permission_base)

    if not db_permission:
        return R.err(user_id=current_user.id, msg='查询权限失败，指定权限不存在')

    return R.ok(user_id=current_user.id, msg='查询权限成功', data=db_permission)


# class QueryByMe(Enum):
#     TENANT = 'tenant
#     NAMESPACE = 'namespace'
#     TOPIC = 'topic'
#     ACTION = 'action'
#     ALL = 'all'


@permission_router.get("/me", summary='查询我拥有的权限')
async def read_my_permissions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_mysql_db),
):
    db_permissions = get_permission_by_username(db=db, username=current_user.username)

    for permission in db_permissions:
        permission.index = db_permissions.index(permission)

    if not db_permissions:
        return R.err(user_id=current_user.id, msg='查询权限失败，本账户无任何访问权限')

    return R.ok(user_id=current_user.id, msg='查询权限成功', data=db_permissions)


@permission_router.get("/me/{tenant}/{namespace}", summary='查询我在指定Namespace下拥有的权限')
async def read_my_permissions_by_namespace(
    tenant: str,
    namespace: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_mysql_db),
):
    db_permissions = get_permission_by_user_tenant_namespace(
        db=db,
        username=current_user.username,
        tenant=tenant,
        namespace=namespace
    )

    for permission in db_permissions:
        permission.index = db_permissions.index(permission)

    if not db_permissions:
        return R.err(user_id=current_user.id, msg='查询权限失败，本账户在指定namespace下无任何访问权限')

    return R.ok(user_id=current_user.id, msg='查询权限成功', data=db_permissions)


@permission_router.get("/me/{tenant}/{namespace}/{topic}", summary='查询我在指定Topic下拥有的权限')
async def read_my_permission_by_namespace_topic(
    tenant: str,
    namespace: str,
    topic: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_mysql_db),
):
    permission_base = PermissionBase(
        username=current_user.username,
        tenant=tenant,
        namespace=namespace,
        topic=topic
    )
    db_permission = get_permission_by_user_tenant_namespace_topic(db=db, permission_base=permission_base)

    if not db_permission:
        return R.err(user_id=current_user.id, msg='查询权限失败，本账户在指定访问方式下无任何访问权限')

    return R.ok(user_id=current_user.id, msg='查询权限成功', data=db_permission)

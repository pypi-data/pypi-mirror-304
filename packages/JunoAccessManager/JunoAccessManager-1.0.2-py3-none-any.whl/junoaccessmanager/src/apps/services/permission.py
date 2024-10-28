from sqlalchemy.orm import Session
from junoaccessmanager.src.apps.models.permission import Permission, TopicActions
from junoaccessmanager.src.apps.schemas.permission import PermissionBase, PermissionCreate


def get_permission_by_id(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_username(db: Session, username: str):
    return db.query(Permission).filter(Permission.username == username).all()


def get_permission_by_tenant(db: Session, tenant: str):
    return db.query(Permission).filter(Permission.tenant == tenant).all()


def get_permission_by_namespace(db: Session, namespace: str):
    return db.query(Permission).filter(Permission.namespace == namespace).all()


def get_permission_by_topic(db: Session, topic: str):
    return db.query(Permission).filter(Permission.topic == topic).all()


def get_permission_by_action(db: Session, action: TopicActions):
    return db.query(Permission).filter(Permission.action == action).all()


def get_permission_by_user_tenant(
        db: Session,
        username: str,
        tenant: str
):
    return db.query(Permission) \
        .filter(Permission.username == username) \
        .filter(Permission.tenant == tenant) \
        .all()


def get_permission_by_user_tenant_namespace(
        db: Session,
        username: str,
        tenant: str,
        namespace: str
):
    return db.query(Permission) \
        .filter(Permission.username == username) \
        .filter(Permission.tenant == tenant) \
        .filter(Permission.namespace == namespace) \
        .all()


def get_permission_by_user_tenant_namespace_topic(
        db: Session,
        permission_base: PermissionBase
):
    return db.query(Permission) \
        .filter(Permission.username == permission_base.username) \
        .filter(Permission.tenant == permission_base.tenant) \
        .filter(Permission.namespace == permission_base.namespace) \
        .filter(Permission.topic == permission_base.topic) \
        .first()


def get_all_permissions(db: Session):
    return db.query(Permission).all()


def create_permission(db: Session, permission_create: PermissionCreate):
    try:
        db_permission = Permission(**permission_create.dict())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return True
    except Exception as e:
        return False


def update_permission(db: Session, action: TopicActions, permission_base: PermissionBase):
    try:
        db_permission = get_permission_by_user_tenant_namespace_topic(db=db, permission_base=permission_base)
        if not db_permission:
            return False

        db_permission.action = action
        db.commit()
        return True
    except Exception as e:
        return False


def delete_permission(
        db: Session,
        permission_base: PermissionBase
):
    try:
        db_permission = get_permission_by_user_tenant_namespace_topic(db=db, permission_base=permission_base)
        if not db_permission:
            return False

        db.delete(db_permission)
        db.commit()
        return True
    except Exception as e:
        return False

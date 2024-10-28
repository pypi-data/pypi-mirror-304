from enum import Enum
from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from junoaccessmanager.src.settings import settings
from junoaccessmanager.src.apps.models.user import UserStatusEnum
from junoaccessmanager.src.apps.schemas.user import User, UserCreate
from junoaccessmanager.src.apps.services.user import (
    get_all_users,
    get_user_by_id,
    get_user_by_username,
    create_user,
    update_user,
)
from junoaccessmanager.src.apps.controllers.write_log import write_log
from junoaccessmanager.src.common.dependencies.database import get_mysql_db
from junoaccessmanager.src.common.dependencies.authorization import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_admin_user
)
from junoaccessmanager.src.common.response import R


user_router = APIRouter()


@user_router.post("/me/register", summary='新用户注册')
async def register_user(
        user: UserCreate,
        db: Session = Depends(get_mysql_db)
):
    db_user = get_user_by_username(
        db=db,
        username=user.username
    )

    if db_user:
        return R.err(user_id=-1, msg='注册用户失败，用户名已存在')

    resp = create_user(db=db, user=user)

    if not resp:
        return R.err(user_id=db_user.id, msg='注册用户失败')
    else:
        return R.ok(user_id=resp.id, msg='注册用户成功')


@user_router.post("/me/login", summary='用户登录')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_mysql_db)
):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        return R.err(user_id=-1, msg='用户名或密码错误')
    write_log(user_id=user.id, content='用户登录')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expire_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "status": 200}


@user_router.post("/me/update", summary='用户信息更新')
async def edit_user(
    username: str,
    password: str,
    email: str | None = None,
    phone: str | None = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_mysql_db)
):
    user = authenticate_user(db=db, username=username, password=password)
    if not user:
        return R.err(user_id=current_user.id, msg='更新本账户信息失败，用户名或密码错误')

    kwargs = {}
    if email:
        kwargs.update({'email': email})
    if phone:
        kwargs.update({'phone': phone})

    resp = update_user(db=db, username=username, **kwargs)

    if resp:
        return R.ok(user_id=current_user.id, msg='更新本账户信息成功')
    else:
        return R.err(user_id=current_user.id, msg='更新本账户信息失败')


@user_router.get("/me", summary='我的信息')
async def me(current_user: User = Depends(get_current_active_user)):
    return R.ok(user_id=current_user.id, msg='查找本账户信息成功', data=current_user.__dict__)


@user_router.post("/admin/update", summary='【管理员】更新指定用户信息')
async def edit_user(
    username: str,
    new_password: str | None = None,
    new_email: str | None = None,
    new_phone: str | None = None,
    new_status: UserStatusEnum | None = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_mysql_db)
):
    kwargs = {}
    if new_password:
        kwargs.update({'password': new_password})
    if new_email:
        kwargs.update({'email': new_email})
    if new_phone:
        kwargs.update({'phone': new_phone})

    resp = update_user(db=db, username=username, status=new_status, **kwargs)

    if resp:
        return R.ok(user_id=current_user.id, msg='更新用户信息成功')
    else:
        return R.err(user_id=current_user.id, msg='更新用户信息失败')


class QueryBy(Enum):
    USER_ID = 'user_id'
    USERNAME = 'username'
    ALL = 'all'


@user_router.get("/admin/query", summary='【管理员】读取指定用户信息')
async def read_user(
    query_by: QueryBy,
    query_value: int | str | None = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_mysql_db)
):

    if query_by == QueryBy.USER_ID:
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询用户失败，缺少查询参数')
        db_users = [get_user_by_id(db=db, id=query_value)]
    elif query_by == QueryBy.USERNAME:
        db_users = [get_user_by_username(db=db, username=query_value)]
        if not query_value:
            return R.err(user_id=current_user.id, msg='查询用户失败，缺少查询参数')
    else:
        if query_value:
            return R.err(user_id=current_user.id, msg='查询用户失败，查询参数多余')
        db_users = get_all_users(db=db)

    if not db_users or not db_users[0]:
        return R.err(user_id=current_user.id, msg='查询用户失败，指定用户不存在')

    return R.ok(user_id=current_user.id, msg='查询用户成功', data=db_users)

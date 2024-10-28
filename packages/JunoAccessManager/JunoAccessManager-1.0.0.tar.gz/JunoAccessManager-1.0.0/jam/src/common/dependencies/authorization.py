from typing import Union
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from jam.src.apps.schemas.user import User
from jam.src.apps.services.user import get_user_by_username, verify_password_hash
from jam.src.common.dependencies.database import get_mysql_db
from jam.src.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/me/login")


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password_hash(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expire_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    if not expire_delta:
        expire_delta = timedelta(minutes=15)
    expire = datetime.now() + expire_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_mysql_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # if current_user.status == models.user.UserStatusEnum.InActivated or current_user.status == models.user.UserStatusEnum.WaitActivation:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.username != 'admin':
        raise HTTPException(status_code=400, detail="UNAUTHORIZED USER")
    return current_user


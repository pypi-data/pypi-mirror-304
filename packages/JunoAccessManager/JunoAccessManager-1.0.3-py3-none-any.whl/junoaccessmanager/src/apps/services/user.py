import traceback
from typing import Dict
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from junoaccessmanager.src.apps.models.user import User, UserStatusEnum
from junoaccessmanager.src.apps.schemas.user import UserCreate
from junoaccessmanager.src.apps.controllers.pulsar_manage import create_mq_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()  # type: ignore


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()  # type: ignore


def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()  # type: ignore


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_all_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict.pop('password')
        db_user = User(**user_dict, hashed_password=hashed_password, mq_token=create_mq_token(user_dict['username']))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        user = db.query(User).filter(User.username == user.username).first()
        return user
    except Exception as e:
        return False


def update_user(
        db: Session,
        username: str,
        status: UserStatusEnum | None = None,
        **kwargs: Dict[str, str]
):
    try:
        db_user = db.query(User).filter(User.username == username).first()  # type: ignore

        if not db_user:
            raise HTTPException(status_code=400, detail="租户名称不存在")

        if status:
            db_user.status = status

        if 'password' in kwargs:
            hashed_password = get_password_hash(kwargs['password'])
            db_user.hashed_password = hashed_password

        if 'email' in kwargs:
            db_user.email = kwargs['email']

        if 'phone' in kwargs:
            db_user.phone = kwargs['phone']

        db.commit()
        db.refresh(db_user)
        return True
    except Exception as e:
        raise False

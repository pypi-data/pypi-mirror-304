import traceback

import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy.orm import Session

from junoaccessmanager.src.apps.models.log import Log
from junoaccessmanager.src.apps.schemas.log import LogCreate


def get_log_by_id(db: Session, log_id: int):
    return db.query(Log).filter(Log.id == log_id).first()


def get_log_by_user_id(db: Session, user_id: int):
    return db.query(Log).filter(Log.user_id == user_id).all()


def create_log(db: Session, log: LogCreate):
    try:
        db_log = Log(**log.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    except sqlalchemy.exc.IntegrityError as e:
        err = traceback.format_exc()
        print(err)
        raise HTTPException(status_code=400, detail="数据库内部执行失败")
    except Exception as e:
        err = traceback.format_exc()
        print(err)
        raise HTTPException(status_code=400, detail="在数据库中新增日志失败")

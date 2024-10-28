from junoaccessmanager.src.apps.services.log import create_log
from junoaccessmanager.src.apps.schemas.log import LogCreate
from junoaccessmanager.src.core.database import SessionLocal_mysql


def write_log(user_id: int, content: str):
    log_create = LogCreate(
        user_id=user_id,
        content=content
    )
    create_log(db=SessionLocal_mysql(), log=log_create)

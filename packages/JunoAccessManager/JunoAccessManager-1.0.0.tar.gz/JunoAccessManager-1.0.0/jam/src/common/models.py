from datetime import datetime
from jam.src.core.database import Base_mysql
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(Base_mysql):
    __abstract__ = True

    id = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True, comment="自增ID"
    )
    create_time: Mapped[datetime] = mapped_column(
        default=func.now(),
        insert_default=func.now(),
        comment="创建时间",
        index=True,
    )
    update_time: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


def to_dict(self):
    data_dict = {}
    for c in self.__table__.columns:
        value = getattr(self, c.name, None)
        if value:
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
        data_dict[c.name] = value
    return data_dict


Base_mysql.to_dict = to_dict

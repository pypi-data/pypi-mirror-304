from pydantic import BaseModel


class LogBase(BaseModel):
    user_id: int
    content: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int

    class Config:
        from_attributes = True


# class Logs(Log):
#     index: int = 0

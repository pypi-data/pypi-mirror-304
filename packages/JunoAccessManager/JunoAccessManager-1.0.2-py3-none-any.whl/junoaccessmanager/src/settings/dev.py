from .base import Settings


class DevSettings(Settings):
    APP_DEBUG: bool = True
    RUNNING_PORT: int = 8000
    # 日志配置
    LOG_LEVEL: int = 10

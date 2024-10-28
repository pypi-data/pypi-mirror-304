from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
    )

    # 项目基础配置
    APP_DEBUG: bool = False
    RUNNING_PORT: int = 80
    APP_HOST: str = "0.0.0.0"
    PROJECT_VERSION: str = "2.0.0"
    PROJECT_NAME: str = "JunoAccess 项目"
    PROJECT_SUMMARY: str = "JunoAccess 项目后端接口与自控通讯服务"
    PROJECT_DESCRIPTION: str = "JunoAccess 项目后端接口与自控通讯服务, 基于FastAPI和APScheduler开发。"
    BASE_DIR: Path = Path(__file__).parent.parent.parent

    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # 分页
    PAGINATION_SIZE: int = 10
    PAGINATION_MAX_SIZE: int = 50

    # 数据库配置
    SQLALCHEMY_MYSQL_DATABASE_URL: str

    # 日志配置 10 ,20 ,30 ,40 50
    LOG_LEVEL: int = 10
    LOG_FORMAT: str = (
        "<green><b>{time:YYYY-MM-DD HH:mm:ss.SSS}</b></green> | "
        "<level>{level:8}</level> | "
        "<level>{traceid}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # access token 配置
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 后端接口前缀
    API_PREFIX: str = "api"
    ENV: str = "dev"

    # Pulsar 管理控制
    PULSAR_HOST: str = 'pulsar://192.168.2.24:6650'
    PULSAR_ADMIN_HOST: str = 'http://192.168.2.24:8080/admin/v2'
    PULSAR_ADMIN_TOKEN: str = 'eyJhbGciOiJSUzI1NiIsInR5cCI6bnVsbH0.eyJzdWIiOiJhZG1pbiJ9.mhtCQY7cCSk3JhY09xT6BZ0-T--CHO1w1jkbsmGFVj2OolLTNIWTnZNdvw3qRrb9sM6479lXgnZrxMV4aMR58TqY3R3OnObcLx_-f4e5DHG9yB2GDFxmd-C5-jZJBLK2mpjvaSJdSprqlZirz7KWbrXBjMzIfiJVpLmG8leX9t7uAhK6biklPsViMtBEShUGXAHnHUHalHqM_LxawlnMOVFfWJRKXEKRB9F1e9AXUsD8E7QxCUXPqFwoAeGJeKmLCzHpCQalj4u0HseHsN-AgLP5GZ7JJL820Fpz3vMJXJsha7PcUEqd4QmTMrD70r8EbxaJTSexH5b4gj3Vb__EVw'


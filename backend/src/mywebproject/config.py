from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from mywebproject.resource.path import ENV_FILE


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    APP_NAME: str = Field(default="mywebproject", description="应用名称")
    APP_VERSION: str = Field(default="0.1.0", description="应用版本")
    APP_ENV: Literal["dev", "test", "prod"] = Field(
        default="dev", description="运行环境"
    )
    DEBUG: bool = Field(default=False, description="是否开启调试模式")

    BACKEND_URL: str = Field(default="0.0.0.0", description="后端的地址")
    BACKEND_PORT: int = Field(default=8000, description="后端的端口号")
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173"], description="允许跨域的前端地址"
    )

    DATABASE_URL: str = Field(description="MySQL/MariaDB 数据库连接地址")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]

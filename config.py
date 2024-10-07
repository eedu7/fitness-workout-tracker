import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    MYSQL_URL: str | None = os.getenv("MYSQL_URL")
    JWT_SECRET_KEY: str | None = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str | None = os.getenv("JWT_ALGORITHM")
    JWT_EXP: int | None = os.getenv("JWT_EXP")
    PAGINATION_MAX_LIMIT: int | None = os.getenv("PAGINATION_MAX_LIMIT")


config: Config = Config()

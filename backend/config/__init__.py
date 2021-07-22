import secrets
import os
from typing import List, Union
from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    SERVER_NAME: str = os.environ.get("SERVER_NAME", "PartyFiller Backend")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    API_HOSTNAME: AnyHttpUrl = os.environ.get("API_HOSTNAME", "http://localhost:8000")
    REDIRECT_URL: AnyHttpUrl = os.environ.get("REDIRECT_URL", API_HOSTNAME)
    SITE_HOSTNAME: AnyHttpUrl = os.environ.get("SITE_HOSTNAME", "http://localhost:3000")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [str(API_HOSTNAME), str(SITE_HOSTNAME)]
    DISCORD_CLIENT_ID: str = os.environ.get("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET: str = os.environ.get("DISCORD_CLIENT_SECRET")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "NO TOKEN")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_SERVER: str = "db"
    DATABASE_USER: str = os.environ.get("DB_USER")
    DATABASE_PASSWORD: str = os.environ.get("DB_PASS")
    DATABASE_NAME: str = os.environ.get("DB_NAME")

    ORIGINS: List[AnyHttpUrl] = [
        os.environ.get("API_HOSTNAME", "http://localhost:8800"),
        os.environ.get("SITE_HOSTNAME", "http://localhost:3001"),
        "http://localhost",
        "http://localhost:8800",
        "http://localhost:3001"
    ]

    SUPERUSERS: List[str] = os.environ.get(
        "SUPERUSERS", "1234567890"
    )

    @validator("SUPERUSERS", pre=True)
    def assemble_superusers(cls, v: Union[str, List[str]]) -> Union[
        List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(" ")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()

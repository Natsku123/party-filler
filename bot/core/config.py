import os
import logging
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    TOKEN: str = os.environ.get("TOKEN")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_HOST: str = os.environ.get("DB_HOST", "db")
    SITE_HOSTNAME: AnyHttpUrl = os.environ.get(
        "SITE_HOSTNAME", "http://party.hellshade.fi"
    )

    class Config:
        case_sensitive = True


settings = Settings()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


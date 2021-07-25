from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any
from sqlalchemy.ext.declarative import as_declarative
from config import settings


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{username}:{password}@{server}/{db}".format(
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    server=settings.DATABASE_SERVER,
    db=settings.DATABASE_NAME,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id: Any
    __name__: str

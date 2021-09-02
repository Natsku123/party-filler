from sqlmodel import create_engine, Table, Column, Integer, ForeignKey, SQLModel, Field
from sqlalchemy.orm import sessionmaker
from typing import Any, Optional
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

relationship_settings = {}


@as_declarative()
class Base:
    id: Any
    __name__: str


# class PlayerServerLink(SQLModel, table=True):
#     player_id: Optional[int] = Field(foreign_key="player.id")
#     server_id: Optional[int] = Field(foreign_key="server.id")


player_server_association = Table(
    "players_servers",
    SQLModel.metadata,
    Column("player_id", Integer, ForeignKey("player.id")),
    Column("server_id", Integer, ForeignKey("server.id")),
)

from typing import Optional
from sqlmodel import Field, SQLModel

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)


class Channel(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    name: str = Field(sa_column=Column(String(255), nullable=False))
    discord_id: str = Field(sa_column=Column(String(64), nullable=False, unique=True))
    server_id: int = Field(
        sa_column=Column(Integer, ForeignKey("servers.id"), nullable=False)
    )

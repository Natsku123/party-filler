from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from core.database import player_server_association


class Server(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    name: str = Field(sa_column=Column(String(255), nullable=False))
    icon: str = Field(sa_column=Column(String(64)))
    discord_id: str = Field(sa_column=Column(String(64), nullable=False, unique=True))
    channels: List["Channel"] = Relationship(
        sa_relationship=relationship("Channel", backref=backref("server", lazy=True))
    )
    players: List["Player"] = Relationship(
        sa_relationship=relationship(
            "Player", secondary=player_server_association, back_populates="servers"
        )
    )

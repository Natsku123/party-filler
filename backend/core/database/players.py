from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from core.database import player_server_association


class Player(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    discord_id: str = Field(sa_column=Column(String(64), nullable=False, unique=True))
    name: str = Field(sa_column=Column(String(64), nullable=False))
    discriminator: str = Field(sa_column=Column(String(4), nullable=False))
    icon: str = Field(sa_column=Column(String(64)))

    servers: List["Server"] = Relationship(
        sa_relationship=relationship(
            "Server", secondary=player_server_association, back_populates="players"
        )
    )

    def dict(self):
        return {
            "id": self.id,
            "discord_id": self.discord_id,
            "name": self.name,
            "discriminator": self.discriminator,
            "icon": self.icon,
        }

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
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of player",
    )
    discord_id: str = Field(
        sa_column=Column(String(64), nullable=False, unique=True),
        alias="discordId",
        description="ID on discord",
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False),
        description="Discord username of player",
    )
    discriminator: str = Field(
        sa_column=Column(String(4), nullable=False),
        description="Discord user discriminator",
    )
    icon: Optional[str] = Field(
        sa_column=Column(String(64)), description="Discord icon hash"
    )

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


class PlayerCreate(SQLModel):
    discord_id: str = Field(alias="discordId", description="ID on discord")
    name: str = Field(description="Discord username of player")
    discriminator: str = Field(description="Discord user discriminator")
    icon: Optional[str] = Field(None, description="Discord icon hash")


class PlayerUpdate(SQLModel):
    discord_id: Optional[str] = Field(
        None, alias="discordId", description="ID on discord"
    )
    name: Optional[str] = Field(None, description="Discord username of player")
    discriminator: Optional[str] = Field(None, description="Discord user discriminator")
    icon: Optional[str] = Field(None, description="Discord icon hash")


class PlayerShort(SQLModel):
    id: int = Field(description="ID of player")
    discord_id: str = Field(alias="discordId", description="ID on discord")
    name: str = Field(description="Discord username of player")
    discriminator: str = Field(description="Discord user discriminator")
    icon: Optional[str] = Field(None, description="Discord icon hash")

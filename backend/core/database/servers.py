from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from core.database import player_server_association, relationship_settings

if TYPE_CHECKING:
    from .players import Player
    from .channels import Channel


class Server(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of server",
    )
    name: str = Field(
        sa_column=Column(String(255), nullable=False),
        description="Name of server from Discord",
    )
    icon: Optional[str] = Field(
        sa_column=Column(String(64)), description="Icon of server from Discord"
    )
    discord_id: str = Field(
        sa_column=Column(String(64), nullable=False, unique=True),
        alias="discordId",
        description="Discord ID of server",
    )
    channels: List["Channel"] = Relationship(
        sa_relationship=relationship(
            "Channel", back_populates="server", **relationship_settings
        )
    )
    players: List["Player"] = Relationship(
        sa_relationship=relationship(
            "Player",
            secondary=player_server_association,
            back_populates="servers",
            **relationship_settings
        )
    )


class ServerCreate(SQLModel):
    name: str = Field(description="Name of server from Discord")
    icon: Optional[str] = Field(None, description="Icon of server from Discord")
    discord_id: str = Field(alias="discordId", description="Discord ID of server")


class ServerUpdate(SQLModel):
    name: Optional[str] = Field(None, description="Name of server from Discord")
    icon: Optional[str] = Field(None, description="Icon of server from Discord")
    discord_id: Optional[str] = Field(
        None, alias="discordId", description="Discord ID of server"
    )


class ServerShort(SQLModel):
    id: int = Field(description="ID of server")
    name: str = Field(description="Name of server from Discord")
    icon: Optional[str] = Field(None, description="Icon of server from Discord")
    discord_id: str = Field(alias="discordId", description="Discord ID of server")

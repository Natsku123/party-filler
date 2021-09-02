from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from core.database import relationship_settings

if TYPE_CHECKING:
    from .models import Server, ServerShort


class Channel(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of channel",
    )
    name: str = Field(
        sa_column=Column(String(255), nullable=False),
        description="Name of channel from Discord",
    )
    discord_id: str = Field(
        sa_column=Column(String(64), nullable=False, unique=True),
        alias="discordId",
        description="Discord ID of channel",
    )
    server_id: int = Field(
        sa_column=Column(Integer, ForeignKey("server.id"), nullable=False),
        alias="serverId",
        description="ID of server associated with",
    )
    server: "Server" = Relationship(sa_relationship_kwargs=relationship_settings)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelShort(SQLModel):
    id: int = Field(
        description="ID of channel",
    )
    name: str = Field(
        description="Name of channel from Discord",
    )
    discord_id: str = Field(
        alias="discordId",
        description="Discord ID of channel",
    )
    server_id: int = Field(
        alias="serverId",
        description="ID of server associated with",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelCreate(SQLModel):
    name: Optional[str] = Field(None, description="Name of channel from Discord")
    discord_id: str = Field(..., alias="discordId", description="Discord ID of channel")
    server_id: Optional[int] = Field(
        None, alias="serverId", description="ID of server associated with"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelUpdate(SQLModel):
    name: Optional[str] = Field(None, description="Name of channel from Discord")
    discord_id: Optional[str] = Field(
        None, alias="discordId", description="Discord ID of channel"
    )
    server_id: Optional[int] = Field(
        None, alias="serverId", description="ID of server associated with"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelRead(SQLModel):
    id: int = Field(
        description="ID of channel",
    )
    name: str = Field(
        description="Name of channel from Discord",
    )
    discord_id: str = Field(
        alias="discordId",
        description="Discord ID of channel",
    )
    server_id: int = Field(
        alias="serverId",
        description="ID of server associated with",
    )
    server: "ServerShort"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

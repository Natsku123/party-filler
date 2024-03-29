from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from core.database import INTEGER_SIZE

if TYPE_CHECKING:
    from .models import Server, ServerShort


class Channel(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of channel",
        gt=0,
        le=INTEGER_SIZE,
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
        gt=0,
        le=INTEGER_SIZE,
    )
    server: "Server" = Relationship()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelShort(SQLModel):
    id: int = Field(description="ID of channel", gt=0, le=INTEGER_SIZE)
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
        gt=0,
        le=INTEGER_SIZE,
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelCreate(SQLModel):
    name: Optional[str] = Field(None, description="Name of channel from Discord")
    discord_id: str = Field(..., alias="discordId", description="Discord ID of channel")
    server_id: Optional[int] = Field(
        None,
        alias="serverId",
        description="ID of server associated with",
        gt=0,
        le=INTEGER_SIZE,
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
        None,
        alias="serverId",
        description="ID of server associated with",
        gt=0,
        le=INTEGER_SIZE,
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ChannelRead(SQLModel):
    id: int = Field(description="ID of channel", gt=0, le=INTEGER_SIZE)
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
        gt=0,
        le=INTEGER_SIZE,
    )
    server: "ServerShort"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

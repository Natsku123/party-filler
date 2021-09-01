from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)


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
    server: "Server" = Relationship(sa_relationship=relationship("Server"))


class ChannelShort(SQLModel):
    id: Optional[int] = Field(
        None,
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


class ChannelCreate(SQLModel):
    name: Optional[str] = Field(None, description="Name of channel from Discord")
    discord_id: str = Field(..., alias="discordId", description="Discord ID of channel")
    server_id: Optional[int] = Field(
        None, alias="serverId", description="ID of server associated with"
    )


class ChannelUpdate(SQLModel):
    name: Optional[str] = Field(None, description="Name of channel from Discord")
    discord_id: Optional[str] = Field(
        None, alias="discordId", description="Discord ID of channel"
    )
    server_id: Optional[int] = Field(
        None, alias="serverId", description="ID of server associated with"
    )

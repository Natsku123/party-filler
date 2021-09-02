from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from .models import Player, PlayerShort, Channel, ChannelShort


class Server(SQLModel, table=True):
    id: Optional[int] = Field(
        description="ID of server",
    )
    name: str = Field(
        description="Name of server from Discord",
    )
    icon: Optional[str] = Field(description="Icon of server from Discord")
    discord_id: str = Field(
        alias="discordId",
        description="Discord ID of server",
    )
    channels: List["Channel"] = []
    players: List["Player"] = []

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ServerCreate(SQLModel):
    name: str = Field(description="Name of server from Discord")
    icon: Optional[str] = Field(None, description="Icon of server from Discord")
    discord_id: str = Field(alias="discordId", description="Discord ID of server")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ServerUpdate(SQLModel):
    name: Optional[str] = Field(None, description="Name of server from Discord")
    icon: Optional[str] = Field(None, description="Icon of server from Discord")
    discord_id: Optional[str] = Field(
        None, alias="discordId", description="Discord ID of server"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ServerShort(SQLModel):
    id: int = Field(description="ID of server")
    name: str = Field(description="Name of server from Discord")
    icon: Optional[str] = Field(None, description="Icon of server from Discord")
    discord_id: str = Field(alias="discordId", description="Discord ID of server")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ServerRead(SQLModel):
    id: int = Field(
        description="ID of server",
    )
    name: str = Field(
        description="Name of server from Discord",
    )
    icon: Optional[str] = Field(description="Icon of server from Discord")
    discord_id: str = Field(
        alias="discordId",
        description="Discord ID of server",
    )
    channels: List["ChannelShort"] = []
    players: List["PlayerShort"] = []

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

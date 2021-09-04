from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from core.database import player_server_association

if TYPE_CHECKING:
    from .models import Server, ServerShort


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
        # sa_relationship_kwargs=relationship_settings, back_populates="players"
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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlayerCreate(SQLModel):
    discord_id: str = Field(alias="discordId", description="ID on discord")
    name: str = Field(description="Discord username of player")
    discriminator: str = Field(description="Discord user discriminator")
    icon: Optional[str] = Field(None, description="Discord icon hash")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlayerUpdate(SQLModel):
    discord_id: Optional[str] = Field(
        None, alias="discordId", description="ID on discord"
    )
    name: Optional[str] = Field(None, description="Discord username of player")
    discriminator: Optional[str] = Field(None, description="Discord user discriminator")
    icon: Optional[str] = Field(None, description="Discord icon hash")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlayerShort(SQLModel):
    id: int = Field(description="ID of player")
    discord_id: str = Field(alias="discordId", description="ID on discord")
    name: str = Field(description="Discord username of player")
    discriminator: str = Field(description="Discord user discriminator")
    icon: Optional[str] = Field(None, description="Discord icon hash")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlayerRead(SQLModel):
    id: int = Field(
        description="ID of player",
    )
    discord_id: str = Field(
        alias="discordId",
        description="ID on discord",
    )
    name: str = Field(
        description="Discord username of player",
    )
    discriminator: str = Field(
        description="Discord user discriminator",
    )
    icon: Optional[str] = Field(description="Discord icon hash")

    servers: List["ServerShort"] = []

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

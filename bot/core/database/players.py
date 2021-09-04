from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from .models import Server, ServerShort


class Player(SQLModel):
    id: Optional[int] = Field(
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

    servers: List["Server"] = []

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

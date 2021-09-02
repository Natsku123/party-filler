from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from .models import Party, PartyShort


class Role(SQLModel):
    id: Optional[int] = Field(
        description="ID of role",
    )
    party_id: Optional[int] = Field(
        gt=0,
        alias="partyId",
        description="ID of party",
    )
    name: Optional[str] = Field(description="Name of role")
    max_players: Optional[int] = Field(
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    party: Optional["Party"] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleCreate(SQLModel):
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players of role"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleUpdate(SQLModel):
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players of role"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleShort(SQLModel):
    id: int = Field(description="ID of role")
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players of role"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleRead(SQLModel):
    id: int = Field(
        description="ID of role",
    )
    party_id: Optional[int] = Field(
        gt=0,
        alias="partyId",
        description="ID of party",
    )
    name: Optional[str] = Field(description="Name of role")
    max_players: Optional[int] = Field(
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    party: Optional["PartyShort"] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

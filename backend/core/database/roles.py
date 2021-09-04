from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from core.database import INTEGER_SIZE

if TYPE_CHECKING:
    from .models import Party, PartyShort


class Role(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of role",
        gt=0,
        le=INTEGER_SIZE,
    )
    party_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("party.id")),
        gt=0,
        le=INTEGER_SIZE,
        alias="partyId",
        description="ID of party",
    )
    name: Optional[str] = Field(
        sa_column=Column(String(64)), description="Name of role"
    )
    max_players: Optional[int] = Field(
        sa_column=Column(Integer),
        gt=0,
        le=INTEGER_SIZE,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    party: Optional["Party"] = Relationship(
        sa_relationship=relationship("Party", back_populates="roles")
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleCreate(SQLModel):
    party_id: Optional[int] = Field(
        None, gt=0, le=INTEGER_SIZE, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None,
        gt=0,
        le=INTEGER_SIZE,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleUpdate(SQLModel):
    party_id: Optional[int] = Field(
        None, gt=0, le=INTEGER_SIZE, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None,
        gt=0,
        le=INTEGER_SIZE,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleShort(SQLModel):
    id: int = Field(description="ID of role", gt=0, le=INTEGER_SIZE)
    party_id: Optional[int] = Field(
        None, gt=0, le=INTEGER_SIZE, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None,
        gt=0,
        le=INTEGER_SIZE,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RoleRead(SQLModel):
    id: int = Field(description="ID of role", gt=0, le=INTEGER_SIZE)
    party_id: Optional[int] = Field(
        gt=0,
        le=INTEGER_SIZE,
        alias="partyId",
        description="ID of party",
    )
    name: Optional[str] = Field(description="Name of role")
    max_players: Optional[int] = Field(
        gt=0,
        le=INTEGER_SIZE,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    party: Optional["PartyShort"] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

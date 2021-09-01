from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey


class Role(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of role",
    )
    party_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("party.id")),
        gt=0,
        alias="partyId",
        description="ID of party",
    )
    name: Optional[str] = Field(
        sa_column=Column(String(64)), description="Name of role"
    )
    max_players: Optional[int] = Field(
        sa_column=Column(Integer),
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players of role",
    )

    party: Optional["Party"] = Relationship(
        sa_relationship=relationship("Party", backref=backref("roles", lazy=True))
    )


class RoleCreate(SQLModel):
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players of role"
    )


class RoleUpdate(SQLModel):
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players of role"
    )


class RoleShort(SQLModel):
    id: int = Field(description="ID of role")
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    name: Optional[str] = Field(None, description="Name of role")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players of role"
    )

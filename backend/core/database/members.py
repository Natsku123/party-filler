from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from core.database import relationship_settings

if TYPE_CHECKING:
    from .parties import Party
    from .players import Player
    from .roles import Role


class Member(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of member",
    )
    player_req: Optional[int] = Field(
        None,
        sa_column=Column(Integer),
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play",
    )
    party_id: int = Field(
        sa_column=Column(Integer, ForeignKey("party.id"), nullable=False),
        gt=0,
        alias="partyId",
        description="ID of party",
    )
    player_id: int = Field(
        sa_column=Column(Integer, ForeignKey("player.id"), nullable=False),
        gt=0,
        alias="playerId",
        description="ID of player",
    )
    role_id: Optional[int] = Field(
        None,
        sa_column=Column(Integer, ForeignKey("role.id"), nullable=True),
        gt=0,
        alias="roleId",
        description="ID of role",
    )

    party: "Party" = Relationship(
        sa_relationship_kwargs=relationship_settings, back_populates="members"
    )
    player: "Player" = Relationship(sa_relationship_kwargs=relationship_settings)
    role: Optional["Role"] = Relationship(sa_relationship_kwargs=relationship_settings)


class MemberCreate(SQLModel):
    player_req: Optional[int] = Field(
        None,
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play",
    )
    party_id: int = Field(gt=0, alias="partyId", description="ID of party")
    player_id: int = Field(gt=0, alias="playerId", description="ID of player")
    role_id: Optional[int] = Field(None, gt=0, alias="roleId", description="ID of role")


class MemberUpdate(SQLModel):
    player_req: Optional[int] = Field(
        None,
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play",
    )
    party_id: Optional[int] = Field(
        None, gt=0, alias="partyId", description="ID of party"
    )
    player_id: Optional[int] = Field(
        None, gt=0, alias="playerId", description="ID of player"
    )
    role_id: Optional[int] = Field(None, gt=0, alias="roleId", description="ID of role")


class MemberShort(SQLModel):
    id: int = Field(..., description="ID of member")
    player_req: Optional[int] = Field(
        None,
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play",
    )
    party_id: int = Field(gt=0, alias="partyId", description="ID of party")
    player_id: int = Field(gt=0, alias="playerId", description="ID of player")
    role_id: Optional[int] = Field(None, gt=0, alias="roleId", description="ID of role")

    player: "Player"
    role: Optional["Role"] = None

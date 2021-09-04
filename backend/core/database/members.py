from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, Integer, ForeignKey

if TYPE_CHECKING:
    from .models import Party, PartyShort, Player, PlayerShort, Role, RoleShort


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
        sa_relationship_kwargs={"lazy": "joined"}, back_populates="members"
    )
    player: "Player" = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    role: Optional["Role"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class MemberShort(SQLModel):
    id: int = Field(description="ID of member")
    player_req: Optional[int] = Field(
        None,
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play",
    )
    party_id: int = Field(gt=0, alias="partyId", description="ID of party")
    player_id: int = Field(gt=0, alias="playerId", description="ID of player")
    role_id: Optional[int] = Field(None, gt=0, alias="roleId", description="ID of role")

    player: "PlayerShort"
    role: Optional["RoleShort"] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class MemberRead(SQLModel):
    id: int = Field(
        description="ID of member",
    )
    player_req: Optional[int] = Field(
        None,
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play",
    )
    party_id: int = Field(
        gt=0,
        alias="partyId",
        description="ID of party",
    )
    player_id: int = Field(
        gt=0,
        alias="playerId",
        description="ID of player",
    )
    role_id: Optional[int] = Field(
        None,
        gt=0,
        alias="roleId",
        description="ID of role",
    )

    party: "PartyShort"
    player: "PlayerShort"
    role: Optional["RoleShort"] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

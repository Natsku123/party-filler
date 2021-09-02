from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean

from core.database import relationship_settings

if TYPE_CHECKING:
    from .channels import Channel
    from .players import Player
    from .members import Member
    from .games import Game
    from .roles import Role


class Party(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of party",
    )
    title: str = Field(
        sa_column=Column(String(255), nullable=False), description="Title of party"
    )
    leader_id: int = Field(
        sa_column=Column(Integer, ForeignKey("player.id")),
        gt=0,
        alias="leaderId",
        description="ID of party leader",
    )
    game_id: int = Field(
        sa_column=Column(Integer, ForeignKey("game.id")),
        gt=0,
        alias="gameId",
        description="ID of game to be played",
    )
    max_players: Optional[int] = Field(
        sa_column=Column(Integer),
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players",
    )
    min_players: Optional[int] = Field(
        sa_column=Column(Integer),
        gt=0,
        alias="minPlayers",
        description="Minimum number of players",
    )
    description: Optional[str] = Field(
        sa_column=Column(Text()), description="Description of party"
    )
    channel_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("channel.id")),
        gt=0,
        alias="channelId",
        description="ID of channel",
    )
    start_time: Optional[datetime] = Field(
        sa_column=Column(DateTime),
        alias="startTime",
        description="Party search start time",
    )
    end_time: Optional[datetime] = Field(
        sa_column=Column(DateTime), alias="endTime", description="Party search end time"
    )
    locked: bool = Field(
        sa_column=Column(Boolean, default=False),
        alias="locked",
        description="Party locked status",
    )

    channel: Optional["Channel"] = Relationship(
        sa_relationship_kwargs=relationship_settings
    )
    leader: "Player" = Relationship(sa_relationship_kwargs=relationship_settings)
    members: List["Member"] = Relationship(sa_relationship_kwargs=relationship_settings)
    roles: List["Role"] = Relationship(sa_relationship_kwargs=relationship_settings)
    game: "Game" = Relationship(sa_relationship_kwargs=relationship_settings)


#     @root_validator
#     def check_min_and_max_players(cls, values):
#         min_p, max_p = values.get("min_players"), values.get("max_players")
#         if min_p is not None and max_p is not None and min_p > max_p:
#             raise ValueError(
#                 "Maximum number of players cannot " "be less than the minimum!"
#             )
#         return values

#     @root_validator
#     def check_times(cls, values):
#         start, end = values.get("start_time"), values.get("end_time")
#         if start is not None and end is not None and start > end:
#             raise ValueError("Start time cannot be greater than end time")
#
#         return values


class PartyCreate(SQLModel):
    title: str = Field(description="Title of party")
    leader_id: int = Field(gt=0, alias="leaderId", description="ID of party leader")
    game_id: int = Field(gt=0, alias="gameId", description="ID of game to be played")
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players"
    )
    min_players: Optional[int] = Field(
        None, gt=0, alias="minPlayers", description="Minimum number of players"
    )
    description: Optional[str] = Field(None, description="Description of party")
    channel_id: Optional[int] = Field(
        None, gt=0, alias="channelId", description="ID of channel"
    )
    start_time: Optional[datetime] = Field(
        None, alias="startTime", description="Party search start time"
    )
    end_time: Optional[datetime] = Field(
        None, alias="endTime", description="Party search end time"
    )


class PartyUpdate(SQLModel):
    title: Optional[str] = Field(None, description="Title of party")
    leader_id: Optional[int] = Field(
        None, gt=0, alias="leaderId", description="ID of party leader"
    )
    game_id: Optional[int] = Field(
        None, gt=0, alias="gameId", description="ID of game to be played"
    )
    max_players: Optional[int] = Field(
        None, gt=0, alias="maxPlayers", description="Maximum number of players"
    )
    min_players: Optional[int] = Field(
        None, gt=0, alias="minPlayers", description="Minimum number of players"
    )
    description: Optional[str] = Field(None, description="Description of party")
    channel_id: Optional[int] = Field(
        None, gt=0, alias="channelId", description="ID of channel"
    )
    start_time: Optional[datetime] = Field(
        None, alias="startTime", description="Party search start time"
    )
    end_time: Optional[datetime] = Field(
        None, alias="endTime", description="Party search end time"
    )


class PartyShort(SQLModel):
    id: Optional[int] = Field(description="ID of party")
    title: str = Field(description="Title of party")
    leader_id: int = Field(gt=0, alias="leaderId", description="ID of party leader")
    game_id: int = Field(gt=0, alias="gameId", description="ID of game to be played")
    max_players: Optional[int] = Field(
        gt=0, alias="maxPlayers", description="Maximum number of players"
    )
    min_players: Optional[int] = Field(
        gt=0, alias="minPlayers", description="Minimum number of players"
    )
    description: Optional[str] = Field(description="Description of party")
    channel_id: Optional[int] = Field(
        gt=0, alias="channelId", description="ID of channel"
    )
    start_time: Optional[datetime] = Field(
        alias="startTime", description="Party search start time"
    )
    end_time: Optional[datetime] = Field(
        alias="endTime", description="Party search end time"
    )
    locked: bool = Field(alias="locked", description="Party locked status")

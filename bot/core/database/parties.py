from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel
from datetime import datetime

if TYPE_CHECKING:
    from .models import (
        Channel,
        ChannelShort,
        Player,
        PlayerShort,
        Member,
        MemberShort,
        Game,
        GameShort,
        Role,
        RoleShort,
    )


class Party(SQLModel):
    id: Optional[int] = Field(
        description="ID of party",
    )
    title: str = Field(description="Title of party")
    leader_id: int = Field(
        gt=0,
        alias="leaderId",
        description="ID of party leader",
    )
    game_id: int = Field(
        gt=0,
        alias="gameId",
        description="ID of game to be played",
    )
    max_players: Optional[int] = Field(
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players",
    )
    min_players: Optional[int] = Field(
        gt=0,
        alias="minPlayers",
        description="Minimum number of players",
    )
    description: Optional[str] = Field(description="Description of party")
    channel_id: Optional[int] = Field(
        gt=0,
        alias="channelId",
        description="ID of channel",
    )
    start_time: Optional[datetime] = Field(
        alias="startTime",
        description="Party search start time",
    )
    end_time: Optional[datetime] = Field(
        alias="endTime", description="Party search end time"
    )
    locked: bool = Field(
        alias="locked",
        description="Party locked status",
    )

    channel: Optional["Channel"] = None
    leader: "Player"
    members: List["Member"] = []
    roles: List["Role"] = []
    game: "Game"

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
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PartyRead(SQLModel):
    id: int = Field(
        description="ID of party",
    )
    title: str = Field(description="Title of party")
    leader_id: int = Field(
        gt=0,
        alias="leaderId",
        description="ID of party leader",
    )
    game_id: int = Field(
        gt=0,
        alias="gameId",
        description="ID of game to be played",
    )
    max_players: Optional[int] = Field(
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players",
    )
    min_players: Optional[int] = Field(
        gt=0,
        alias="minPlayers",
        description="Minimum number of players",
    )
    description: Optional[str] = Field(description="Description of party")
    channel_id: Optional[int] = Field(
        gt=0,
        alias="channelId",
        description="ID of channel",
    )
    start_time: Optional[datetime] = Field(
        alias="startTime",
        description="Party search start time",
    )
    end_time: Optional[datetime] = Field(
        alias="endTime", description="Party search end time"
    )
    locked: bool = Field(
        alias="locked",
        description="Party locked status",
    )

    channel: Optional["ChannelShort"] = None
    leader: "PlayerShort"
    members: List["MemberShort"] = []
    roles: List["RoleShort"] = []
    game: "GameShort"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

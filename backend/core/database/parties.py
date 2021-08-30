from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean


class Party(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    title: str = Field(sa_column=Column(String(255), nullable=False))
    leader_id: int = Field(sa_column=Column(Integer, ForeignKey("players.id")))
    game_id: int = Field(sa_column=Column(Integer, ForeignKey("games.id")))
    max_players: int = Field(sa_column=Column(Integer))
    min_players: int = Field(sa_column=Column(Integer))
    description: str = Field(sa_column=Column(Text()))
    channel_id: int = Field(sa_column=Column(Integer, ForeignKey("channels.id")))
    start_time: datetime = Field(sa_column=Column(DateTime))
    end_time: datetime = Field(sa_column=Column(DateTime))
    locked: bool = Field(sa_column=Column(Boolean, default=False))

    channel: Optional["Channel"] = Relationship(
        sa_relationship=relationship("Channel", lazy="joined")
    )
    leader: "Player" = Relationship(
        sa_relationship=relationship("Player", lazy="joined")
    )
    members: List["Member"] = Relationship(sa_relationship=relationship("Member"))
    game: "Game" = Relationship(sa_relationship=relationship("Game", lazy="joined"))

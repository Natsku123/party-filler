from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String


class Game(SQLModel, table=True):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, unique=True),
        description="ID of game",
    )
    name: str = Field(
        sa_column=Column(String(255), nullable=False), description="Name of game"
    )
    default_max_players: int = Field(
        sa_column=Column(Integer),
        gt=0,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GameCreate(SQLModel):
    name: str = Field(description="Name of game")
    default_max_players: int = Field(
        gt=0,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GameUpdate(SQLModel):
    name: Optional[str] = Field(None, description="Name of game")
    default_max_players: Optional[int] = Field(
        None,
        gt=0,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GameShort(SQLModel):
    id: int = Field(description="ID of game")
    name: str = Field(description="Name of game")
    default_max_players: int = Field(
        gt=0,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GameRead(SQLModel):
    id: int = Field(
        description="ID of game",
    )
    name: str = Field(description="Name of game")
    default_max_players: int = Field(
        gt=0,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

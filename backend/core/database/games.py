from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String


class Game(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    name: str = Field(sa_column=Column(String(255), nullable=False))
    default_max_players: int = Field(sa_column=Column(Integer))

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey


class Role(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    party_id: int = Field(sa_column=Column(Integer, ForeignKey("parties.id")))
    name: str = Field(sa_column=Column(String(64)))
    max_players: int = Field(sa_column=Column(Integer))

    party: "Party" = Relationship(
        sa_relationship=relationship("Party", backref=backref("roles", lazy=True))
    )

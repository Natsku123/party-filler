from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey


class Member(SQLModel):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, unique=True))
    player_req: int = Field(sa_column=Column(Integer))
    party_id: int = Field(
        sa_column=Column(Integer, ForeignKey("parties.id"), nullable=False)
    )
    player_id: int = Field(
        sa_column=Column(Integer, ForeignKey("players.id"), nullable=False)
    )
    role_id: int = Field(
        sa_column=Column(Integer, ForeignKey("roles.id"), nullable=True)
    )

    party: "Party" = Relationship(
        sa_relationship=relationship("Party", lazy="joined", back_populates="members")
    )
    player: "Player" = Relationship(
        sa_relationship=relationship("Player", lazy="joined")
    )
    role: Optional["Role"] = Relationship(
        sa_relationship=relationship("Role", lazy="joined")
    )

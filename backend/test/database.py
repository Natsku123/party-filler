import pytest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from core.database import models
from test import *


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    with Session(engine) as db:

        test_player = (
            db.query(models.Player)
            .filter(models.Player.discord_id == "1234567890")
            .first()
        )

        if not test_player:
            test_player = models.Player(
                discord_id="1234567890", name="TEST PLAYER 1", discriminator="0001"
            )
            db.add(test_player)
            db.commit()
            db.refresh(test_player)

    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session, test_player

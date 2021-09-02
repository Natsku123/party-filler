from fastapi import HTTPException, Depends
from sqlmodel import create_engine, Session, SQLModel

from core.database import models, crud
from test import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def get_testing_get_db():
    with Session(engine) as session:
        yield session


def get_testing_current_user(
    db: Session = Depends(get_testing_get_db),
) -> models.Player:

    user = crud.player.get(db, id=1)
    if not user:
        raise HTTPException(status_code=404, detail="Player not found")

    return user


def init_test_db():
    SQLModel.metadata.create_all(bind=engine)

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

    return test_player

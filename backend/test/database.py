from fastapi import Request, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.database import Base, models, crud
from test import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_testing_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_testing_current_user(db: Session = Depends(get_testing_get_db)) -> models.Player:

    user = crud.player.get(db, id=1)
    if not user:
        raise HTTPException(status_code=404, detail="Player not found")

    return user


def init_test_db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    test_player = db.query(models.Player).filter(
            models.Player.discord_id == "1234567890"
    ).first()

    if not test_player:
        test_player = models.Player(
            discord_id="1234567890",
            name="TEST PLAYER 1",
            discriminator="0001"
        )
        db.add(test_player)
        db.commit()
        db.refresh(test_player)

    db.close()

    return test_player




from fastapi import Request, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.database import Base, models, crud

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def testing_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def testing_current_user(db: Session = Depends(testing_get_db)) -> models.Player:

    user = crud.player.get(db, id=1)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def init_test_db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    test_player = models.Player(

    )
    db.add(db)
    db.commit()
    db.refresh(test_player)

    return test_player




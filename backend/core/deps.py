from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

from .database import crud, models
from core.database import engine


def get_db():
    with Session(engine) as session:
        yield session


# def get_db():
# db = SessionLocal()
# try:
#    yield db
# finally:
#    db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.Player:
    player = request.session.get("user", None)

    if player is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    if "id" not in player:
        raise HTTPException(status_code=400, detail="Invalid session")

    user = crud.player.get(db, id=player["id"])
    if not user:
        raise HTTPException(status_code=404, detail="Player not found")

    return user

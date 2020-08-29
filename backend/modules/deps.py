from typing import Generator

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from . import models
from . import crud
from .database import SessionLocal, engine


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.Player:
    player = request.session.get('user', None)

    if player is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    if 'id' not in player:
        raise HTTPException(status_code=400, detail="Invalid session")

    user = crud.player.get(db, id=player['id'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

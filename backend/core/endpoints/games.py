from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import deps
from core.database import crud, models, schemas
from core.utils import is_superuser

router = APIRouter()


@router.get("/", response_model=List[schemas.Game], tags=["games"])
def get_games(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    return crud.game.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Game, tags=["games"])
def create_game(
    *,
    db: Session = Depends(deps.get_db),
    game: schemas.GameCreate,
    current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.game.create(db, obj_in=game)


@router.put("/{id}", response_model=schemas.Game, tags=["games"])
def update_game(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    game: schemas.GameUpdate,
    current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_game = crud.game.get(db=db, id=id)

    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not current_user and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_game = crud.game.update(db=db, db_obj=db_game, obj_in=game)
    return db_game


@router.get("/{id}", response_model=schemas.Game, tags=["games"])
def get_game(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    game = crud.game.get(db=db, id=id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.delete("/{id}", response_model=schemas.Game, tags=["games"])
def delete_game(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    game = crud.game.get(db=db, id=id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not current_user and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.game.remove(db=db, id=id)

    return game

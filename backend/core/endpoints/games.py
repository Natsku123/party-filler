from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from core import deps
from core.database import crud, INTEGER_SIZE
from core.database.models import GameCreate, GameUpdate, GameRead, Player
from core.utils import is_superuser

from core.endpoints import get_multi_responses as gmr, generic_responses as gr

router = APIRouter()


@router.get("/", response_model=List[GameRead], tags=["games"], responses={**gmr, **gr})
def get_games(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, le=INTEGER_SIZE, ge=0, description="Skip N objects"),
    limit: int = Query(
        100,
        le=INTEGER_SIZE,
        ge=0,
        description="Limit the number of objects returned by N",
    ),
    filters: Optional[str] = Query(None, alias="filter"),
    order: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
) -> Any:
    return crud.game.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=GameRead, tags=["games"], responses={**gr})
def create_game(
    *,
    db: Session = Depends(deps.get_db),
    game: GameCreate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.game.create(db, obj_in=game)


@router.put("/{id}", response_model=GameRead, tags=["games"], responses={**gr})
def update_game(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of game"),
    game: GameUpdate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    db_game = crud.game.get(db=db, id=id)

    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not current_user and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_game = crud.game.update(db=db, db_obj=db_game, obj_in=game)
    return db_game


@router.get("/{id}", response_model=GameRead, tags=["games"], responses={**gr})
def get_game(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of game")
) -> Any:
    game = crud.game.get(db=db, id=id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.delete("/{id}", response_model=GameRead, tags=["games"], responses={**gr})
def delete_game(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of game"),
    current_user: Player = Depends(deps.get_current_user),
    force: bool = Query(False, description="Force deletion")
) -> Any:
    game = crud.game.get(db=db, id=id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not current_user and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    # if not force and len(game.parties) > 0:
    #     raise HTTPException(status_code=400, detail="Warning! Game is used by some parties, deletion will delete the parties also! Use force to continue.")

    crud.game.remove(db=db, id=id)

    return game

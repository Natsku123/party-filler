from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import deps
from core.database import crud, models, schemas

router = APIRouter()


@router.get('/', response_model=schemas.Player, tags=["players"])
def get_current_player(
        *,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")

    return current_user


@router.get('/{id}', response_model=schemas.Player, tags=["players"])
def get_player(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    player = crud.player.get(db=db, id=id)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@router.put('/{id}', response_model=schemas.Player, tags=["players"])
def update_player(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        player: schemas.PlayerUpdate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_player = crud.player.get(db=db, id=id)

    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")

    if db_player.id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    db_player = crud.player.update(db=db, db_obj=db_player, obj_in=player)
    return db_player


@router.delete('/{id}', response_model=schemas.Player, tags=["players"])
def delete_player(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    player = crud.player.get(db=db, id=id)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if player.id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.player.remove(db=db, id=id)

    return player

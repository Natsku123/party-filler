from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import deps
from core.database import crud, models, schemas

router = APIRouter()


@router.get('/', response_model=List[schemas.Server], tags=["servers"])
def get_servers(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    return crud.server.get_multi(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Server, tags=["servers"])
def create_server(
        *,
        db: Session = Depends(deps.get_db),
        server: schemas.ServerCreate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.server.create(db, obj_in=server)


@router.put('/{id}', response_model=schemas.Server, tags=["servers"])
def update_server(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        server: schemas.ServerUpdate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_server = crud.server.get(db=db, id=id)

    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    if db_server not in current_user.servers:
        raise HTTPException(status_code=401, detail="Not authorized")

    db_server = crud.server.update(db=db, db_obj=db_server, obj_in=server)
    return db_server


@router.get('/{id}', response_model=schemas.Server, tags=["servers"])
def get_server(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return server


@router.delete('/{id}', response_model=schemas.Server, tags=["servers"])
def delete_server(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if server not in current_user.servers:
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.server.remove(db=db, id=id)

    return server


@router.get(
    '/{id}/channels',
    response_model=List[schemas.Channel],
    tags=["servers", "channels"]
)
def get_channels(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        skip: int = 0,
        limit: int = 100
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return crud.channel.get_multi_by_server(
        db,
        server_id=id,
        skip=skip,
        limit=limit
    )

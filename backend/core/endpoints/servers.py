from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from core import deps
from core.database import crud, INTEGER_SIZE
from core.database.models import (
    ServerCreate,
    ServerUpdate,
    ServerRead,
    Player,
    ChannelRead,
)
from core.utils import is_superuser

from core.endpoints import get_multi_responses as gmr, generic_responses as gr

router = APIRouter()


@router.get(
    "/", response_model=List[ServerRead], tags=["servers"], responses={**gmr, **gr}
)
def get_servers(
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
    return crud.server.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=ServerRead, tags=["servers"], responses={**gr})
def create_server(
    *,
    db: Session = Depends(deps.get_db),
    server: ServerCreate,
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    db_servers = crud.server.get_multi(db, filters={"discord_id": server.discord_id})

    if len(db_servers) > 0:
        raise HTTPException(status_code=400, detail="Server already exists")

    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.server.create(db, obj_in=server)


@router.put("/{id}", response_model=ServerRead, tags=["servers"], responses={**gr})
def update_server(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of server"),
    server: ServerUpdate,
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    db_server = crud.server.get(db=db, id=id)

    if db_server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    if server.discord_id != db_server.discord_id:
        db_servers = crud.server.get_multi(
            db, filters={"discord_id": server.discord_id}
        )

        if len(db_servers) > 0:
            raise HTTPException(status_code=400, detail="Server already exists")

    db_server = crud.server.update(db=db, db_obj=db_server, obj_in=server)
    return db_server


@router.get("/{id}", response_model=ServerRead, tags=["servers"], responses={**gr})
def get_server(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of server"),
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return server


@router.delete("/{id}", response_model=ServerRead, tags=["servers"], responses={**gr})
def delete_server(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of server"),
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.server.remove(db=db, id=id)

    return server


@router.get(
    "/{id}/channels",
    response_model=List[ChannelRead],
    tags=["servers"],
    responses={**gr},
)
def get_channels(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of server"),
    skip: int = Query(0, le=INTEGER_SIZE, ge=0, description="Skip N objects"),
    limit: int = Query(
        100,
        le=INTEGER_SIZE,
        ge=0,
        description="Limit the number of objects returned by N",
    ),
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return crud.channel.get_multi_by_server(db, server_id=id, skip=skip, limit=limit)

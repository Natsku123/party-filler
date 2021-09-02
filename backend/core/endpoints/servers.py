from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from core import deps
from core.database import crud
from core.database.players import Player
from core.database.channels import ChannelRead
from core.database.servers import ServerCreate, ServerUpdate, ServerRead
from core.utils import is_superuser

router = APIRouter()


@router.get("/", response_model=List[ServerRead], tags=["servers"])
def get_servers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    filters: Optional[str] = Query(None, alias="filter"),
    order: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
) -> Any:
    return crud.server.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=ServerRead, tags=["servers"])
def create_server(
    *,
    db: Session = Depends(deps.get_db),
    server: ServerCreate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.server.create(db, obj_in=server)


@router.put("/{id}", response_model=ServerRead, tags=["servers"])
def update_server(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    server: ServerUpdate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    db_server = crud.server.get(db=db, id=id)

    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    if db_server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_server = crud.server.update(db=db, db_obj=db_server, obj_in=server)
    return db_server


@router.get("/{id}", response_model=ServerRead, tags=["servers"])
def get_server(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return server


@router.delete("/{id}", response_model=ServerRead, tags=["servers"])
def delete_server(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.server.remove(db=db, id=id)

    return server


@router.get(
    "/{id}/channels", response_model=List[ChannelRead], tags=["servers", "channels"]
)
def get_channels(
    *, db: Session = Depends(deps.get_db), id: int, skip: int = 0, limit: int = 100
) -> Any:
    server = crud.server.get(db=db, id=id)

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return crud.channel.get_multi_by_server(db, server_id=id, skip=skip, limit=limit)

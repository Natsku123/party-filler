from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from core import deps
from core.database import crud
from core.database.roles import Role, RoleCreate, RoleUpdate
from core.database.players import Player
from core.utils import is_superuser

router = APIRouter()


@router.get("/", response_model=List[Role], tags=["roles"])
def get_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    filters: Optional[str] = Query(None, alias="filter"),
    order: Optional[Union[str, List[str]]] = None,
    group: Optional[Union[str, List[str]]] = None,
) -> Any:
    return crud.role.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=Role, tags=["roles"])
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role: RoleCreate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.role.create(db, obj_in=role)


@router.put("/{id}", response_model=Role, tags=["roles"])
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    role: RoleUpdate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    db_role = crud.role.get(db=db, id=id)

    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    if (
        db_role.party
        and db_role.party.leader_id != current_user.id
        and not is_superuser(current_user)
    ):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_role = crud.role.update(db=db, db_obj=db_role, obj_in=role)
    return db_role


@router.get("/{id}", response_model=Role, tags=["roles"])
def get_role(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    role = crud.role.get(db=db, id=id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


@router.delete("/{id}", response_model=Role, tags=["roles"])
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    role = crud.role.get(db=db, id=id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if (
        role.party
        and role.party.leader_id != current_user.id
        and not is_superuser(current_user)
    ):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.role.remove(db=db, id=id)

    return role

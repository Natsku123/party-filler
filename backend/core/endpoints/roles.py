from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from core import deps
from core.database import crud, INTEGER_SIZE
from core.database.models import RoleCreate, RoleUpdate, RoleRead, Player
from core.utils import is_superuser

from core.endpoints import get_multi_responses as gmr, generic_responses as gr

router = APIRouter()


@router.get("/", response_model=List[RoleRead], tags=["roles"], responses={**gmr, **gr})
def get_roles(
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
    return crud.role.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=RoleRead, tags=["roles"], responses={**gr})
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role: RoleCreate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.role.create(db, obj_in=role)


@router.put("/{id}", response_model=RoleRead, tags=["roles"], responses={**gr})
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of role"),
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


@router.get("/{id}", response_model=RoleRead, tags=["roles"], responses={**gr})
def get_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of role")
) -> Any:
    role = crud.role.get(db=db, id=id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


@router.delete("/{id}", response_model=RoleRead, tags=["roles"], responses={**gr})
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of role"),
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

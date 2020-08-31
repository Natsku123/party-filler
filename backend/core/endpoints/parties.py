from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import deps
from core.database import crud, models, schemas

router = APIRouter()


@router.get('/', response_model=List[schemas.Party], tags=["parties"])
def get_parties(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    return crud.party.get_multi(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Party, tags=["parties"])
def create_party(
        *,
        db: Session = Depends(deps.get_db),
        party: schemas.PartyCreate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.party.create(db, obj_in=party)


@router.put('/{id}', response_model=schemas.Party, tags=["parties"])
def update_party(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        party: schemas.PlayerBase,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_party = crud.party.get(db=db, id=id)

    if not db_party:
        raise HTTPException(status_code=404, detail="Party not found")

    if db_party.leader_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    db_party = crud.party.update(db=db, db_obj=db_party, obj_in=party)
    return db_party


@router.get('/{id}', response_model=schemas.Party, tags=["parties"])
def get_party(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return party


@router.delete('/{id}', response_model=schemas.Party, tags=["parties"])
def delete_party(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.leader_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.party.remove(db=db, id=id)

    return party


@router.get(
    '/{id}',
    response_model=List[schemas.Member],
    tags=["parties", "members"]
)
def get_members(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        skip: int = 0,
        limit: int = 100
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return crud.member.get_multi_by_party(
        db, party_id=id, skip=skip, limit=limit
    )

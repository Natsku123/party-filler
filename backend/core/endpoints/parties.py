import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core import deps
from core.database import crud, models, schemas
from core.utils import datetime_to_string, is_superuser

from worker import send_webhook

router = APIRouter()


@router.get("/", response_model=List[schemas.Party], tags=["parties"])
def get_parties(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    return crud.party.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Party, tags=["parties"])
def create_party(
    *,
    db: Session = Depends(deps.get_db),
    party: schemas.PartyCreate,
    current_user: models.Player = Depends(deps.get_current_user),
    notify: bool = Query(False),
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    party = crud.party.create(db, obj_in=party)

    # Create leader as member
    leader_member = schemas.MemberCreate(
        **{
            "party_id": party.id,
            "player_id": party.leader_id,
        }
    )
    crud.member.create(db, obj_in=leader_member)
    db.refresh(party)

    # Send webhook to bot if notification wanted
    if notify and party.channel:
        webhook_data = {
            "party": party,

            "event": {
                "name": "on_party_create",
                "timestamp": datetime_to_string(datetime.datetime.now()),
            },
        }
        webhook = schemas.PartyCreateWebhook(**webhook_data)

        send_webhook.delay("http://bot:9080/webhook", webhook.json())

    return party


@router.put("/{id}", response_model=schemas.Party, tags=["parties"])
def update_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    party: schemas.PlayerUpdate,
    current_user: models.Player = Depends(deps.get_current_user),
) -> Any:
    db_party = crud.party.get(db=db, id=id)

    if not db_party:
        raise HTTPException(status_code=404, detail="Party not found")

    if db_party.leader_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_party = crud.party.update(db=db, db_obj=db_party, obj_in=party)
    return db_party


@router.get("/{id}", response_model=schemas.Party, tags=["parties"])
def get_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return party


@router.delete("/{id}", response_model=schemas.Party, tags=["parties"])
def delete_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.Player = Depends(deps.get_current_user),
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.leader_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.party.remove(db=db, id=id)

    return party


@router.get(
    "/{id}/players", response_model=List[schemas.Member], tags=["parties", "members"]
)
def get_members(
    *, db: Session = Depends(deps.get_db), id: int, skip: int = 0, limit: int = 100
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return crud.member.get_multi_by_party(db, party_id=id, skip=skip, limit=limit)

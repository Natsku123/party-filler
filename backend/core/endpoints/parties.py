import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from core import deps
from core.database import crud, schemas
from core.database.players import Player
from core.database.parties import Party, PartyCreate, PartyUpdate
from core.database.members import Member, MemberCreate
from core.utils import datetime_to_string, is_superuser

from worker import send_webhook

router = APIRouter()


@router.get("/", response_model=List[Party], tags=["parties"])
def get_parties(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    filters: Optional[str] = Query(None, alias="filter"),
    order: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
) -> Any:
    return crud.party.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=Party, tags=["parties"])
def create_party(
    *,
    db: Session = Depends(deps.get_db),
    party: PartyCreate,
    current_user: Player = Depends(deps.get_current_user),
    notify: bool = Query(False),
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    party = crud.party.create(db, obj_in=party)

    # Create leader as member
    leader_member = MemberCreate(
        party_id=party.id,
        player_id=party.leader_id,
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


@router.put("/{id}", response_model=Party, tags=["parties"])
def update_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    party: PartyUpdate,
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    db_party = crud.party.get(db=db, id=id)

    if not db_party:
        raise HTTPException(status_code=404, detail="Party not found")

    if db_party.leader_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_party = crud.party.update(db=db, db_obj=db_party, obj_in=party)
    return db_party


@router.get("/{id}", response_model=Party, tags=["parties"])
def get_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return party


@router.delete("/{id}", response_model=Party, tags=["parties"])
def delete_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.leader_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.party.remove(db=db, id=id)

    return party


@router.get("/{id}/players", response_model=List[Member], tags=["parties", "members"])
def get_members(
    *, db: Session = Depends(deps.get_db), id: int, skip: int = 0, limit: int = 100
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return crud.member.get_multi_by_party(db, party_id=id, skip=skip, limit=limit)

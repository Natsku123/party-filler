import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from core import deps
from core.database import crud, schemas, INTEGER_SIZE
from core.database.models import (
    PartyCreate,
    PartyUpdate,
    PartyRead,
    Player,
    MemberCreate,
    MemberRead,
)
from core.utils import datetime_to_string, is_superuser

from core.endpoints import get_multi_responses as gmr, generic_responses as gr

from worker import send_webhook

router = APIRouter()


@router.get(
    "/", response_model=List[PartyRead], tags=["parties"], responses={**gmr, **gr}
)
def get_parties(
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
    return crud.party.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=PartyRead, tags=["parties"], responses={**gr})
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

    leader = crud.player.get(db, party.leader_id)

    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")

    if party.game_id:
        game = crud.game.get(db, party.game_id)

        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

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
        webhook = schemas.PartyCreateWebhook.parse_obj(webhook_data)

        send_webhook.delay("http://bot:9080/webhook", webhook.json())

    return party


@router.put("/{id}", response_model=PartyRead, tags=["parties"], responses={**gr})
def update_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of party"),
    party: PartyUpdate,
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    db_party = crud.party.get(db=db, id=id)

    if not db_party:
        raise HTTPException(status_code=404, detail="Party not found")

    if db_party.leader_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    leader = crud.player.get(db, party.leader_id)

    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")

    if party.game_id:
        game = crud.game.get(db, party.game_id)

        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

    db_party = crud.party.update(db=db, db_obj=db_party, obj_in=party)
    return db_party


@router.get("/{id}", response_model=PartyRead, tags=["parties"], responses={**gr})
def get_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of party"),
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return party


@router.delete("/{id}", response_model=PartyRead, tags=["parties"], responses={**gr})
def delete_party(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of party"),
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.leader_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.party.remove(db=db, id=id)

    return party


@router.get(
    "/{id}/players", response_model=List[MemberRead], tags=["parties"], responses={**gr}
)
def get_members(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of party"),
    skip: int = Query(0, le=INTEGER_SIZE, ge=0, description="Skip N objects"),
    limit: int = Query(
        100,
        le=INTEGER_SIZE,
        ge=0,
        description="Limit the number of objects returned by N",
    ),
) -> Any:
    party = crud.party.get(db=db, id=id)

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    return crud.member.get_multi_by_party(db, party_id=id, skip=skip, limit=limit)

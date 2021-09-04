import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from core import deps
from core.database import crud, schemas, INTEGER_SIZE
from core.database.models import MemberCreate, MemberUpdate, MemberRead, Player
from core.utils import datetime_to_string, is_superuser

from core.endpoints import get_multi_responses as gmr, generic_responses as gr

from worker import send_webhook

router = APIRouter()


@router.get(
    "/", response_model=List[MemberRead], tags=["members"], responses={**gmr, **gr}
)
def get_members(
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
    return crud.member.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=MemberRead, tags=["members"], responses={**gr})
def create_member(
    *,
    db: Session = Depends(deps.get_db),
    member: MemberCreate,
    current_user: Player = Depends(deps.get_current_user),
    notify: bool = Query(False),
) -> Any:
    if not current_user or (
        current_user.id != member.player_id and not is_superuser(current_user)
    ):
        raise HTTPException(status_code=401, detail="Not authorized")

    member = crud.member.create(db, obj_in=member)

    # Send webhook to bot if notification wanted
    if notify and member.party.channel:
        webhook_data = {
            "member": member,
            "channel": member.party.channel,
            "event": {
                "name": "on_member_join",
                "timestamp": datetime_to_string(datetime.datetime.now()),
            },
        }
        webhook = schemas.MemberJoinWebhook.parse_obj(webhook_data)

        send_webhook.delay("http://bot:9080/webhook", webhook.json())

    if member.party.channel and len(member.party.members) == member.party.max_players:
        webhook_data = {"party": member.party, "event": {"name": "on_party_full"}}
        webhook = schemas.PartyFullWebhook.parse_obj(webhook_data)

        send_webhook.delay("http://bot:9080/webhook", webhook.json())

        crud.party.lock(db, crud.party.get(db, member.party_id))

    if (
        member.party.channel
        and len(member.party.members) == member.party.min_players
        and member.party.min_players != member.party.max_players
    ):
        webhook_data = {"party": member.party, "event": {"name": "on_party_ready"}}
        webhook = schemas.PartyReadyWebhook.parse_obj(webhook_data)

        send_webhook.delay("http://bot:9080/webhook", webhook.json())

        crud.party.lock(db, crud.party.get(db, member.party_id))

    return member


@router.put("/{id}", response_model=MemberRead, tags=["members"], responses={**gr})
def update_member(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of member"),
    member: MemberUpdate,
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    db_member = crud.member.get(db=db, id=id)

    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    if db_member.player_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_member = crud.member.update(db=db, db_obj=db_member, obj_in=member)
    return db_member


@router.get("/{id}", response_model=MemberRead, tags=["members"], responses={**gr})
def get_member(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of member"),
) -> Any:
    member = crud.member.get(db=db, id=id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@router.delete("/{id}", response_model=MemberRead, tags=["members"], responses={**gr})
def delete_member(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of member"),
    current_user: Player = Depends(deps.get_current_user),
) -> Any:
    member = crud.member.get(db=db, id=id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member.player_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.member.remove(db=db, id=id)

    return member

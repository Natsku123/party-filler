import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import deps
from core.database import crud, models, schemas
from core.utils import send_webhook, datetime_to_string, is_superuser

router = APIRouter()


@router.get('/', response_model=List[schemas.Member], tags=["members"])
def get_members(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    return crud.member.get_multi(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Member, tags=["members"])
def create_member(
        *,
        db: Session = Depends(deps.get_db),
        member: schemas.MemberCreate,
        current_user: models.Player = Depends(deps.get_current_user),
        notify: bool = False
) -> Any:
    if not current_user or \
            (current_user.id != member.player_id and
             not is_superuser(current_user)):
        raise HTTPException(status_code=401, detail="Not authorized")

    member = crud.member.create(db, obj_in=member)

    # Send webhook to bot if notification wanted
    if notify and member.party.channel:
        webhook_data = {
            "member": member,
            "channel": member.party.channel,
            "event": {
                "name": "on_member_join",
                "datetime": datetime_to_string(datetime.datetime.now())
            }
        }
        webhook = schemas.MemberJoinWebhook(**webhook_data)
        try:
            send_webhook(webhook)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Member has been added to the party, but there "
                       f"was an error with the notification: {e}"
            )

    return member


@router.put('/{id}', response_model=schemas.Member, tags=["members"])
def update_member(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        member: schemas.MemberUpdate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_member = crud.member.get(db=db, id=id)

    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    if db_member.player_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_member = crud.member.update(db=db, db_obj=db_member, obj_in=member)
    return db_member


@router.get('/{id}', response_model=schemas.Member, tags=["members"])
def get_member(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    member = crud.member.get(db=db, id=id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@router.delete('/{id}', response_model=schemas.Member, tags=["members"])
def delete_member(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    member = crud.member.get(db=db, id=id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member.player_id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.member.remove(db=db, id=id)

    return member

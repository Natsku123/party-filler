from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import settings

from core import deps
from core.database import crud, models, schemas
from core.utils import is_superuser, get_channel_info

router = APIRouter()


@router.get('/', response_model=List[schemas.Channel], tags=["channels"])
def get_channels(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    return crud.channel.get_multi(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Channel, tags=["channels"])
def create_channel(
        *,
        db: Session = Depends(deps.get_db),
        channel: schemas.ChannelCreate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_channel = db.query(models.Channel).filter(
        models.Channel.discord_id == str(channel.discord_id)
    ).first()

    if db_channel is not None:
        raise HTTPException(status_code=400, detail="Channel already exists")

    if channel.server_id is None or channel.name is None:
        if settings.BOT_TOKEN == "NO TOKEN":
            raise HTTPException(status_code=400, detail="Data not available")

        channel_data = get_channel_info(channel.discord_id)

        if 'code' in channel_data:
            if channel_data['code'] == 50001:
                raise HTTPException(
                    status_code=400,
                    detail="Discord bot has no access to channel"
                )

            raise HTTPException(
                status_code=400, detail="Discord channel not found"
            )
        server = db.query(models.Server).filter(
            models.Server.discord_id == str(channel_data.get('guild_id'))
        ).first()

        if server is None:
            raise HTTPException(status_code=404, detail="Server not found")
        channel = schemas.ChannelCreate(
            **{
                "discordId": channel.discord_id,
                "name": channel_data.get('name'),
                "serverId": server.id
            }
        )

    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")

    return crud.channel.create(db, obj_in=channel)


@router.put('/{id}', response_model=schemas.Channel, tags=["channels"])
def update_channel(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        channel: schemas.ChannelUpdate,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    db_channel = crud.channel.get(db=db, id=id)

    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    db_server = crud.server.get(db=db, id=db_channel.server_id)

    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    if db_server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    if channel.server_id is None or channel.name is None:
        if settings.BOT_TOKEN == "NO TOKEN":
            raise HTTPException(status_code=400, detail="Data not available")

        channel_data = get_channel_info(channel.discord_id)

        if 'code' in channel_data:
            if channel_data['code'] == 50001:
                raise HTTPException(
                    status_code=400,
                    detail="Discord bot has no access to channel"
                )

            raise HTTPException(
                status_code=400, detail="Discord channel not found"
            )
        server = db.query(models.Server).filter(
            models.Server.discord_id == str(channel_data.get('guild_id'))
        ).first()
        channel = schemas.ChannelCreate(
            **{
                "discordId": channel.discord_id,
                "name": channel_data.get('name'),
                "serverId": server.id
            }
        )

    db_channel = crud.channel.update(db=db, db_obj=db_channel, obj_in=channel)
    return db_channel


@router.get('/{id}', response_model=schemas.Channel, tags=["channels"])
def get_channel(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    channel = crud.channel.get(db=db, id=id)

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    return channel


@router.delete('/{id}', response_model=schemas.Channel, tags=["channels"])
def delete_channel(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.Player = Depends(deps.get_current_user)
) -> Any:
    channel = crud.channel.get(db=db, id=id)

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    db_server = crud.server.get(db=db, id=channel.server_id)

    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    if db_server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.channel.remove(db=db, id=id)

    return channel

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from config import settings

from core import deps
from core.database import crud, INTEGER_SIZE
from core.database.models import (
    Player,
    ChannelCreate,
    ChannelUpdate,
    ChannelRead,
)
from core.utils import is_superuser, get_channel_info

from core.endpoints import get_multi_responses as gmr, generic_responses as gr

router = APIRouter()


@router.get(
    "/", response_model=List[ChannelRead], tags=["channels"], responses={**gmr, **gr}
)
def get_channels(
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
    return crud.channel.get_multi(
        db, skip=skip, limit=limit, filters=filters, order=order, group=group
    )


@router.post("/", response_model=ChannelRead, tags=["channels"], responses={**gr})
def create_channel(
    *,
    db: Session = Depends(deps.get_db),
    channel: ChannelCreate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_channels = crud.channel.get_multi(db, filters={"discord_id": channel.discord_id})

    if len(db_channels) > 0:
        raise HTTPException(status_code=400, detail="Channel already exists")

    if channel.server_id is None or channel.name is None:
        if settings.BOT_TOKEN == "NO TOKEN":
            raise HTTPException(status_code=400, detail="Data not available")

        channel_data = get_channel_info(channel.discord_id)

        if "code" in channel_data:
            if channel_data["code"] == 50001:
                raise HTTPException(
                    status_code=400, detail="Discord bot has no access to channel"
                )

            raise HTTPException(status_code=400, detail="Discord channel not found")
        servers = crud.server.get_multi(
            db, filters={"discord_id": str(channel_data.get("guild_id"))}
        )

        if len(servers) == 0:
            raise HTTPException(status_code=404, detail="Server not found")
        channel = ChannelCreate(
            discordId=channel.discord_id,
            name=channel_data.get("name"),
            serverId=servers[0].id,
        )
    else:
        server = crud.server.get(db, channel.server_id)

        if not server:
            raise HTTPException(status_code=404, detail="Server not found")

    return crud.channel.create(db, obj_in=channel)


@router.put("/{id}", response_model=ChannelRead, tags=["channels"], responses={**gr})
def update_channel(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of channel"),
    channel: ChannelUpdate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    db_channel = crud.channel.get(db=db, id=id)

    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    if channel.discord_id != db_channel.discord_id:
        db_channels = crud.channel.get_multi(
            db, filters={"discord_id": channel.discord_id}
        )

        if len(db_channels) > 0:
            raise HTTPException(
                status_code=400, detail="Channel with this Discord ID already exists"
            )

    db_server = crud.server.get(db=db, id=db_channel.server_id)

    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    if db_server not in current_user.servers and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    if channel.server_id is None or channel.name is None:
        if settings.BOT_TOKEN == "NO TOKEN":
            raise HTTPException(status_code=400, detail="Data not available")

        channel_data = get_channel_info(channel.discord_id)

        if "code" in channel_data:
            if channel_data["code"] == 50001:
                raise HTTPException(
                    status_code=400, detail="Discord bot has no access to channel"
                )

            raise HTTPException(status_code=400, detail="Discord channel not found")
        servers = crud.server.get_multi(
            db, filters={"discord_id": str(channel_data.get("guild_id"))}
        )
        if len(servers) == 0:
            raise HTTPException(status_code=404, detail="Server not found")
        channel = ChannelCreate(
            discordId=channel.discord_id,
            name=channel_data.get("name"),
            serverId=servers[0].id,
        )
    elif channel.server_id != db_channel.server_id:
        server = crud.server.get(db, channel.server_id)

        if not server:
            raise HTTPException(status_code=404, detail="Server not found")

    db_channel = crud.channel.update(db=db, db_obj=db_channel, obj_in=channel)
    return db_channel


@router.get("/{id}", response_model=ChannelRead, tags=["channels"], responses={**gr})
def get_channel(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of channel")
) -> Any:
    channel = crud.channel.get(db=db, id=id)

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    return channel


@router.delete("/{id}", response_model=ChannelRead, tags=["channels"], responses={**gr})
def delete_channel(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., le=INTEGER_SIZE, gt=0, description="ID of channel"),
    current_user: Player = Depends(deps.get_current_user)
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

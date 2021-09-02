import main
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core import deps
from core.database import crud, schemas
from core.database.models import (
    Player,
    PlayerUpdate,
    PlayerRead,
    ChannelRead,
    ServerCreate,
    ServerUpdate,
)
from core.utils import is_superuser

router = APIRouter()


@router.get("/", response_model=PlayerRead, tags=["players"])
def get_current_player(*, current_user: Player = Depends(deps.get_current_user)) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")

    return current_user


@router.get("/superuser", response_model=schemas.IsSuperUser, tags=["players"])
def get_is_superuser(*, current_user: Player = Depends(deps.get_current_user)) -> Any:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authorized")

    data = {"isSuperuser": is_superuser(current_user)}
    return schemas.IsSuperUser(**data)


@router.get("/channels", response_model=List[ChannelRead], tags=["channels"])
def get_visible_channels(
    *,
    db: Session = Depends(deps.get_db),
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    servers = current_user.servers
    server_ids = []
    for server in servers:
        server_ids.append(server.id)
    channels = crud.channel.get_multi_by_servers(db, server_ids=server_ids)
    return channels


@router.get("/{id}", response_model=PlayerRead, tags=["players"])
def get_player(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    player = crud.player.get(db=db, id=id)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@router.put("/{id}", response_model=PlayerRead, tags=["players"])
def update_player(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    player: PlayerUpdate,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    db_player = crud.player.get(db=db, id=id)

    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")

    if db_player.id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    db_player = crud.player.update(db=db, db_obj=db_player, obj_in=player)
    return db_player


@router.put("/{id}", response_model=PlayerRead, tags=["players"])
def update_player(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    db_player = crud.player.get(db=db, id=id)

    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")

    if db_player.id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    resp = main.oauth.discord.get("users/@me")
    profile = resp.json()

    if "code" not in profile:
        # Update player info
        player = PlayerUpdate(
            name=profile.get("username"),
            discriminator=profile.get("discriminator"),
            icon=profile.get("avatar"),
        )

        db_player = crud.player.update(db, db_obj=db_player, obj_in=player)

        # Get servers that Player uses
        guilds = main.oauth.discord.get("users/@me/guilds")

        # Create new servers if doesn't already exist or update existing
        for guild in guilds.json():
            server = crud.server.get_by_discord_id(db, discord_id=guild.get("id"))

            if server is None:
                server_obj = ServerCreate(
                    name=guild.get("name"),
                    icon=guild.get("icon"),
                    discordId=guild.get("id"),
                )

                server = crud.server.create(db, obj_in=server_obj)
                db_player.servers.append(server)

            elif server.name != guild.get(
                "name", server.name
            ) or server.icon != guild.get("icon", server.icon):
                server_obj = ServerUpdate(
                    name=guild.get("name"),
                    icon=guild.get("icon"),
                    discordId=guild.get("id"),
                )

                server = crud.server.update(db, db_obj=server, obj_in=server_obj)

        db.commit()
        db.refresh(db_player)


@router.delete("/{id}", response_model=PlayerRead, tags=["players"])
def delete_player(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Player = Depends(deps.get_current_user)
) -> Any:
    player = crud.player.get(db=db, id=id)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if player.id != current_user.id and not is_superuser(current_user):
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.player.remove(db=db, id=id)

    return player

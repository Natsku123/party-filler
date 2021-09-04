from fastapi import FastAPI, Depends, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse

from config import settings
from core.database import SessionLocal
from core.database.models import OAuth2Token, Player, Server
from core.database.schemas import Meta
from sqlalchemy.orm import Session

from core.deps import get_current_user, get_db

from core.endpoints.parties import router as party_router
from core.endpoints.servers import router as server_router
from core.endpoints.channels import router as channel_router
from core.endpoints.players import router as player_router
from core.endpoints.members import router as member_router
from core.endpoints.roles import router as role_router
from core.endpoints.games import router as game_router


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def update_token(name, token, refresh_token=None, access_token=None):

    db = SessionLocal()
    if refresh_token:
        item = (
            db.query(OAuth2Token)
            .filter_by(name=name, refresh_token=refresh_token)
            .first()
        )
    elif access_token:
        item = (
            db.query(OAuth2Token)
            .filter_by(name=name, access_token=access_token)
            .first()
        )
    else:
        db.close()
        return

    # update old token
    item.access_token = token["access_token"]
    item.refresh_token = token.get("refresh_token")
    item.expires_at = token["expires_at"]
    db.add(item)
    db.commit()

    db.close()


oauth = OAuth(update_token=update_token)


def fetch_discord_token(
    current_user: Player = Depends(get_current_user), db: Session = Depends(get_db)
):
    token = (
        db.query(OAuth2Token)
        .filter_by(name="discord", player_id=current_user.id)
        .first()
    )
    if token:
        return token.to_token()


# OAuth with discord setup
oauth.register(
    name="discord",
    client_id=settings.DISCORD_CLIENT_ID,
    client_secret=settings.DISCORD_CLIENT_SECRET,
    access_token_url="https://discord.com/api/oauth2/token",
    access_token_params=None,
    authorize_url="https://discord.com/api/oauth2/authorize",
    authorize_params=None,
    api_base_url="https://discord.com/api/v6",
    client_kwargs={"scope": "identify guilds"},
    fetch_token=fetch_discord_token,
)


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/login")
async def login(request: Request, redirect: str = None):
    redirect_uri = settings.REDIRECT_URL + "/authorize"

    if redirect is None:
        redirect = settings.SITE_HOSTNAME

    request.session["redirect_url"] = redirect

    return await oauth.discord.authorize_redirect(request, redirect_uri)


@app.get("/logout")
async def logout(request: Request):
    redirect_url = settings.SITE_HOSTNAME
    request.session.pop("user", None)
    return RedirectResponse(url=redirect_url)


@app.get("/player_update")
async def player_update(
    player: Player = Depends(get_current_user), db: Session = Depends(get_db)
):
    token = db.query(OAuth2Token).filter_by(player_id=player.id).first()
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    guilds = await oauth.discord.get("users/@me/guilds", token=token.to_token())

    # Create new servers if doesn't already exist
    for guild in guilds.json():
        server = db.query(Server).filter_by(discord_id=guild["id"]).first()
        if server is None:
            server = Server(
                name=guild.get("name"),
                icon=guild.get("icon"),
                discord_id=guild.get("id"),
            )
            db.add(server)
        player.servers.append(server)

    db.add(player)
    db.commit()
    db.refresh(player)

    return {"status": "player updated"}


@app.get("/authorize")
async def authorize(request: Request, db: Session = Depends(get_db)):
    token = await oauth.discord.authorize_access_token(request)

    if token:
        resp = await oauth.discord.get("users/@me", token=token)
    else:
        resp = await oauth.discord.get("users/@me")

    profile = resp.json()

    # Get player
    player = db.query(Player).filter_by(discord_id=profile["id"]).first()

    # If player doesn't exist, create a new one.
    if player is None:
        # logger.debug("Player object" + str(profile))
        player = Player(
            discord_id=profile.get("id"),
            name=profile.get("username"),
            discriminator=profile.get("discriminator"),
            icon=profile.get("avatar"),
        )

        # Get servers that Player uses
        if token:
            guilds = await oauth.discord.get("users/@me/guilds", token=token)
        else:
            guilds = await oauth.discord.get("users/@me/guilds")

        # Create new servers if doesn't already exist
        for guild in guilds.json():
            server = db.query(Server).filter_by(discord_id=guild["id"]).first()
            if server is None:
                server = Server(
                    name=guild.get("name"),
                    icon=guild.get("icon"),
                    discord_id=guild.get("id"),
                )

                db.add(server)
            player.servers.append(server)

        db.add(player)
        db.commit()
        db.refresh(player)

    if token:
        # Update token
        token_obj = db.query(OAuth2Token).filter_by(player_id=player.id).first()
        if token_obj is None:
            token_obj = OAuth2Token(
                player_id=player.id,
                name="discord",
                token_type=token.get("token_type"),
                access_token=token.get("access_token"),
                refresh_token=token.get("refresh_token"),
                expires_at=token.get("expires_at"),
            )
        else:
            token_obj.token_type = (token.get("token_type"),)
            token_obj.access_token = (token.get("access_token"),)
            token_obj.refresh_token = (token.get("refresh_token"),)
            token_obj.expires_at = token.get("expires_at")

        db.add(token_obj)
    db.commit()
    db.refresh(player)

    request.session["user"] = player.dict()

    url = request.session.get("redirect_url")
    if url is None:
        url = settings.SITE_HOSTNAME
    else:
        del request.session["redirect_url"]

    return RedirectResponse(url=url)


@app.get("/meta", response_model=Meta)
def meta():
    return {"version": settings.VERSION, "build": settings.BUILD}


app.include_router(party_router, prefix="/parties")
app.include_router(server_router, prefix="/servers")
app.include_router(channel_router, prefix="/channels")
app.include_router(player_router, prefix="/players")
app.include_router(member_router, prefix="/members")
app.include_router(role_router, prefix="/roles")
app.include_router(game_router, prefix="/games")

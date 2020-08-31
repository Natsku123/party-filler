from fastapi import FastAPI, Depends, Request

from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse

from config import settings
from core.database.models import OAuth2Token, Player, Server
from sqlalchemy.orm import Session

from core.deps import get_current_user, get_db

from core.endpoints.parties import router as party_router
from core.endpoints.servers import router as server_router
from core.endpoints.channels import router as channel_router
from core.endpoints.players import router as player_router


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


# @app.middleware("http")
# async def camel_case(request: Request, call_next):
#     body = await request.json()
#     snake_body = camel_dict_to_snake(request.json())
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

oauth = OAuth()


def fetch_discord_token(current_user: Player = Depends(get_current_user)):
    token = OAuth2Token.query.filter_by(name='discord', player_id=current_user.id).first()
    if token:
        return token.to_token()


# OAuth with discord setup
oauth.register(
    name="discord",
    client_id=settings.DISCORD_CLIENT_ID,
    client_secret=settings.DISCORD_CLIENT_SECRET,
    access_token_url='https://discord.com/api/oauth2/token',
    access_token_params=None,
    authorize_url='https://discord.com/api/oauth2/authorize',
    authorize_params=None,
    api_base_url='https://discord.com/api/v6',
    client_kwargs={'scope': 'identify guilds'},
    fetch_token=fetch_discord_token
)


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.route('/login')
async def login(request: Request, redirect: str = None):
    redirect_uri = settings.API_HOSTNAME + "/authorize"

    if redirect is None:
        redirect = settings.SITE_HOSTNAME

    request.session['redirect_url'] = redirect

    return await oauth.discord.authorize_redirect(request, redirect_uri)


@app.route("/logout")
async def logout(request: Request):
    redirect_url = settings.SITE_HOSTNAME
    request.session.pop('user', None)
    return RedirectResponse(url=redirect_url)


@app.route('/authorize')
async def authorize(request: Request, db: Session = Depends(get_db)):
    token = oauth.discord.authorize_access_token(request)
    resp = oauth.discord.get('users/@me')
    profile = resp.json()

    url = request.session.get('redirect_url')
    if url is None:
        url = settings.SITE_HOSTNAME
    else:
        del request.session['redirect_url']

    # Get player
    player = Player.query.filter_by(discord_id=profile['id']).first()

    # If player doesn't exist, create a new one.
    if player is None:
        #logger.debug("Player object" + str(profile))
        player = Player(
            discord_id=profile.get('id'),
            name=profile.get('username'),
            discriminator=profile.get('discriminator'),
            icon=profile.get('avatar'),
        )

        # Get servers that Player uses
        guilds = oauth.discord.get('users/@me/guilds')

        # Create new servers if doesn't already exist
        for guild in guilds.json():
            server = Server.query.filter_by(discord_id=guild['id']).first()
            if server is None:
                server = Server(
                    name=guild.get('name'),
                    icon=guild.get('icon'),
                    discord_id=guild.get('id')
                )

                # Link server to player
                player.servers.append(server)
                db.add(server)

        db.add(player)

    # Update token
    token_obj = OAuth2Token.query.filter_by(player_id=player.id).first()
    if token_obj is None:
        token_obj = OAuth2Token(
            player_id=player.id,
            name='discord',
            token_type=token.get('token_type'),
            access_token=token.get('access_token'),
            refresh_token=token.get('refresh_token'),
            expires_at=token.get('expires_at')
        )
    else:
        token_obj.token_type = token.get('token_type'),
        token_obj.access_token = token.get('access_token'),
        token_obj.refresh_token = token.get('refresh_token'),
        token_obj.expires_at = token.get('expires_at')

    db.add(token_obj)
    db.commit()
    db.refresh(player)

    request.session['user'] = player.dict()

    return RedirectResponse(url=url)


app.include_router(party_router, prefix="/parties")
app.include_router(server_router, prefix="/servers")
app.include_router(channel_router, prefix="/channels")
app.include_router(player_router, prefix="/players")

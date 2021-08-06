import json
import discord
import logging
from aiohttp.web import RouteTableDef, json_response
from pydantic import ValidationError

from core.api.parser import Parser


routes = RouteTableDef()

# Logging
logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


@routes.get("/")
async def root(request):
    return json_response(
        {"data": "working"}, status=200, content_type="application/json"
    )


@routes.get("/servers")
async def get_servers(request):
    client = request.app["bot"]
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.id)

    return json_response(
        {"servers": guilds}, status=200, content_type="application/json"
    )


@routes.post("/webhook")
async def webhook(request):
    bot = request.app["bot"]

    logger.debug("Incoming webhook... ")

    # Get webhook data
    received_hook = await request.json()
    logger.debug("Webhook data: " + str(received_hook))

    p = Parser(bot)

    try:
        return await p.parse(received_hook)
    except ValidationError as e:
        return json_response(
            json.loads(e.json()), status=422, content_type="application/json"
        )
    except ValueError as e:
        return json_response({"error": e}, status=400, content_type="application/json")
    except discord.Forbidden:
        return json_response(
            {
                "error": "Bot doesn't have permission to send"
                " messages to given channel!"
            },
            status=400,
            content_type="application/json",
        )

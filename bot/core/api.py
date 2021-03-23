import json
import discord
import logging
import dateutil
from aiohttp.web import RouteTableDef, json_response

from core.config import settings

from sqlalchemy import select

routes = RouteTableDef()

# Logging
logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@routes.get('/')
async def root(request):
    return json_response(
        {"data": "working"}, status=200, content_type='application/json'
    )


@routes.get('/servers')
async def get_servers(request):
    client = request.app['bot']
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.id)

    return json_response(
        {"servers": guilds}, status=200, content_type='application/json'
    )


@routes.post('/webhook')
async def webhook(request):
    bot = request.app['bot']

    logger.debug("Incoming webhook... ")

    # Get webhook data
    text = await request.text()
    received_hook = json.loads(text)

    embed = discord.Embed()

    embed.set_author(name="PartyFiller",
                     icon_url=bot.user.avatar_url,
                     url=settings.SITE_HOSTNAME)

    if received_hook.get('event').\
            get('name') == "on_party_create":
        channel_id = int(
            received_hook['party']['channel']['discordId']
        )

        embed.title = received_hook['party']['title']

        # Cut description if too long
        if len(received_hook['party']['description']) > 1000:
            received_hook['party']['description'] = \
                received_hook['party']['description'][:1000]\
                + "..."

        # TODO add join link
        embed.description = f"**{received_hook['party']['leader']['name']}** is looking for more player to play **{received_hook['party']['game']}**.\n{received_hook['party']['description']}"
        embed.add_field(name="Players", value="{0}/{1}".format(
            len(received_hook['party']['members']),
            received_hook['party']['maxPlayers']
        ))

        # Parse time
        if received_hook['party']['startTime'] and received_hook['party']['endTime']:
            start_time = dateutil.parser.parse(received_hook['party']['startTime'])
            end_time = dateutil.parser.parse(received_hook['party']['endTime'])
            duration = end_time - start_time
            str_duration = duration.hours + ":" + duration.minutes + ":" + duration.seconds
            embed.add_field(name="Duration", value="{0}".format(
                str_duration
            ))

        await bot.get_channel(channel_id).send(embed=embed)
    elif received_hook.get('event').get('name') == "on_member_join":
        channel_id = int(received_hook['channel']['discordId'])

        embed.title = "**{0}** joined **{1}**!".format(
            received_hook['member']['player']['name'],
            received_hook['member']['party']['title']
        )

        await bot.get_channel(channel_id).send(embed=embed)
    return json_response({"success": "true"}, status=200, content_type='application/json')

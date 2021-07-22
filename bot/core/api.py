import json
import discord
import logging
from aiohttp.web import RouteTableDef, json_response
from pydantic import ValidationError

from core.database.schemas import PartyCreateWebhook, MemberJoinWebhook, \
    PartyFullWebhook, PartyReadyWebhook

from core.config import settings


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
    received_hook = await request.json()
    logger.debug("Webhook data: " + str(received_hook))

    embed = discord.Embed()

    embed.set_author(name="PartyFiller",
                     icon_url=bot.user.avatar_url,
                     url=settings.SITE_HOSTNAME)

    try:
        if received_hook.get('event').get('name') == "on_party_create":
            event = PartyCreateWebhook.parse_obj(received_hook)

            channel_id = int(event.party.channel.discord_id)

            if bot.get_channel(channel_id) is None:
                raise ValueError("Bot cannot find channel!")

            embed.title = f"***{event.party.leader.name}*** is looking for more players to play ***{event.party.game.name}***!"

            # Cut description if too long
            if len(event.party.description) > 1000:
                event.party.description = \
                    event.party.description[:1000] + "..."

            # TODO add join link
            embed.description = f"**{event.party.title}**\n" \
                                f"{event.party.description}\n" \
                                f"[Join here!]({settings.SITE_HOSTNAME}/#/parties/{event.party.id})"
            embed.add_field(
                name="Players",
                value=f"{len(event.party.members)}/{event.party.max_players}"
            )
            if event.party.end_time and event.party.start_time:
                duration = event.party.end_time - event.party.start_time
                total_sec = duration.total_seconds()

                # Duration to strings
                dh = int(total_sec // (60*60))
                dm = int((total_sec % (60*60)) // 60)
                ds = int((total_sec % (60*60)) % 60)
                str_duration = f"{dh:02}:{dm:02}:{ds:02}"
                embed.add_field(name="Duration", value="{0}".format(
                    str_duration
                ))

            await bot.get_channel(channel_id).send(embed=embed)
        elif received_hook.get('event').get('name') == "on_member_join":

            event = MemberJoinWebhook.parse_obj(received_hook)

            channel_id = int(event.channel.discord_id)

            if bot.get_channel(channel_id) is None:
                raise ValueError("Bot cannot find channel!")

            embed.title = f"**{event.member.player.name}** " \
                          f"joined **{event.member.party.title}**!"

            embed.add_field(
                name="Players",
                value=f"{len(event.member.party.members)}/"
                      f"{event.member.party.max_players}"
            )

            await bot.get_channel(channel_id).send(embed=embed)

        elif received_hook.get('event').get('name') == "on_party_full":

            event = PartyFullWebhook.parse_obj(received_hook)

            channel_id = int(event.party.channel.discord_id)

            if bot.get_channel(channel_id) is None:
                raise ValueError("Bot cannot find channel!")

            embed.title = f"**{event.party.name}** " \
                          f"is full!"

            embed.description = f"**Players**:"

            for member in event.party.members:
                embed.add_field(
                    name=member.player.name,
                    value=member.role.name if member.role else "",
                    inline=False
                )

            await bot.get_channel(channel_id).send(embed=embed)

        elif received_hook.get('event').get('name') == "on_party_ready":

            event = PartyReadyWebhook.parse_obj(received_hook)

            channel_id = int(event.party.channel.discord_id)

            if bot.get_channel(channel_id) is None:
                raise ValueError("Bot cannot find channel!")

            embed.title = f"**{event.party.name}** " \
                          f"is ready!"

            embed.description = f"Party minimum required players reached!" \
                                f"\n\n**Players**:"

            for member in event.party.members:
                embed.add_field(
                    name=member.player.name,
                    value=member.role.name if member.role else "",
                    inline=False
                )

            await bot.get_channel(channel_id).send(embed=embed)
        else:
            return json_response(
                {"error": "Unknown webhook event!"}, status=400,
                content_type='application/json'
            )
        return json_response(
            {"success": "true"}, status=200, content_type='application/json'
        )
    except ValidationError as e:
        return json_response(
            json.loads(e.json()), status=422, content_type='application/json'
        )
    except ValueError as e:
        return json_response(
            {"error": e}, status=400, content_type='application/json'
        )
    except discord.Forbidden:
        return json_response(
            {"error": "Bot doesn't have permission to send"
                      " messages to given channel!"}, status=400,
            content_type='application/json'
        )

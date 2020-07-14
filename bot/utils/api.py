import json
import discord
import datetime
import logging
import dateutil
from aiohttp.web import RouteTableDef, json_response

from utils.tools import get_branch, action_imperfect

routes = RouteTableDef()

# Logging
logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@routes.get('/')
async def root(request):
    return json_response({"data": "working"}, status=200, content_type='application/json')


@routes.get('/servers')
async def get_servers(request):
    client = request.app['bot']
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.id)

    return json_response({"servers": guilds}, status=200, content_type='application/json')


@routes.post('/webhook/{ide}')
async def webhook(request):
    bot = request.app['bot']
    db = request.app['db']
    hook = db.get_webhook(ide=request.match_info['ide'])

    channel_id = 367058034154930196

    logger.debug("Incoming webhook: " + str(request.match_info['ide']))

    # Check if webhook exists
    if hook is not None and hook.get('webhook') is not None:
        hook = hook['webhook']

        # Get webhook data
        text = await request.text()
        jhook = json.loads(text)

        if hook.get('channel', None) is not None:
            channel_id = int(hook['channel'])

        if hook.get('type') == "partyfiller":
            if jhook.get('event').get('name') == "on_party_create":
                channel_id = int(jhook['party']['channel']['discordId'])
                embed = discord.Embed()
                icon_url = bot.user.avatar_url

                embed.set_author(name="PartyFiller",
                                 icon_url=icon_url,
                                 url="http://party.hellshade.fi/")

                embed.title = jhook['party']['title']
                embed.description = "{0} is looking for more player to play {1}." \
                                    "\n{2}".format(
                    jhook['party']['leader']['name'],
                    jhook['party']['game'],
                    jhook['party']['description']
                )
                embed.add_field(name="Players", value="{0}/{1}".format(
                    len(jhook['party']['members']),
                    jhook['party']['maxPlayers']
                ))

                if jhook['party']['startTime'] and jhook['party']['endTime']:
                    start_time = dateutil.parser.parse(jhook['party']['startTime'])
                    end_time = dateutil.parser.parse(jhook['party']['endTime'])
                    duration = end_time - start_time
                    str_duration = duration.hours + ":" + duration.minutes + ":" + duration.seconds
                    embed.add_field(name="Duration", value="{0}".format(
                        str_duration
                    ))

                await bot.get_channel(channel_id).send(embed=embed)
            elif jhook.get('event').get('name') == "on_member_join":
                channel_id = int(jhook['channel']['discordId'])
                embed = discord.Embed()
                icon_url = bot.user.avatar_url

                embed.set_author(name="PartyFiller",
                                 icon_url=icon_url,
                                 url="http://party.hellshade.fi/")

                embed.title = jhook['party']['title']
                embed.description = "{0} is looking for more player to play {1}." \
                                    "\n{2}".format(
                    jhook['party']['leader']['name'],
                    jhook['party']['game'],
                    jhook['party']['description']
                )
                embed.add_field(name="Players", value="{0}/{1}".format(
                    len(jhook['party']['members']),
                    jhook['party']['maxPlayers']
                ))

                if jhook['party']['startTime'] and jhook['party']['endTime']:
                    start_time = dateutil.parser.parse(
                        jhook['party']['startTime'])
                    end_time = dateutil.parser.parse(jhook['party']['endTime'])
                    duration = end_time - start_time
                    str_duration = duration.hours + ":" + duration.minutes + ":" + duration.seconds
                    embed.add_field(name="Duration", value="{0}".format(
                        str_duration
                    ))

                await bot.get_channel(channel_id).send(embed=embed)
        elif hook.get('type', None) == "git":

            embed = discord.Embed()

            icon_url = bot.user.avatar_url

            project = jhook['project']

            # Get icon from project or user
            if project.get('avatar_url', None) is not None:
                icon_url = project['avatar_url']
            elif jhook.get("user_avatar", None) is not None:
                icon_url = jhook['user_avatar']
            elif jhook.get("user", None) is not None:
                if jhook['user'].get("avatar_url", None) is not None:
                    icon_url = jhook['user']['avatar_url']

            # Set author
            embed.set_author(name=project.get('name', "Git"),
                             icon_url=icon_url,
                             url=project['web_url'])

            # Parse git event
            if jhook.get('event_name', None) == "push":
                if jhook['before'][:8] == "00000000":
                    embed.title = "{0} created branch ***{1}*** to ***{2}***".format(
                        jhook['user_name'],
                        get_branch(jhook['ref']),
                        project['path_with_namespace']
                    )
                elif jhook['after'][:8] == "00000000":
                    embed.title = "{0} deleted branch ***{1}*** of ***{2}***".format(
                        jhook['user_name'],
                        get_branch(jhook['ref']),
                        project['path_with_namespace']
                    )
                else:
                    embed.title = "{0} pushed to branch ***{1}*** of ***{2}***".format(
                        jhook['user_name'],
                        get_branch(jhook['ref']),
                        project['path_with_namespace']
                    )

                    embed.description = "Check changes [here]({0}/-/compare/{1}...{2})\n\n".format(
                        project['web_url'],
                        jhook['before'][:8],
                        jhook['after'][:8]
                    )
                    embed.description += "**Commits**:\n"
                    for commit in jhook['commits']:
                        embed.description += "[{0}]({1}): {2}\n".format(
                            commit['id'][:8],
                            commit['url'],
                            commit["title"]
                        )
            elif jhook.get('event_type', None) == "merge_request":
                obj_atr = jhook['object_attributes']
                embed.title = "{0} {1} *!{2} {3}* in ***{4}***".format(
                    jhook['user']['name'],
                    action_imperfect(obj_atr['action']),
                    obj_atr['iid'],
                    obj_atr['title'],
                    project['path_with_namespace']
                )
                embed.description = "{source_branch} -> {target_branch}".format(**obj_atr)
                embed.url = obj_atr['url']

            elif jhook.get('event_type', None) == "issue":
                obj_atr = jhook['object_attributes']
                embed.title = "Issue #{0} {1} {2} by {3}".format(
                    obj_atr['iid'],
                    obj_atr['title'],
                    action_imperfect(obj_atr['action']),
                    jhook['user']['name']
                )
                embed.url = obj_atr['url']
                if obj_atr.get('description', None) is not None:
                    embed.description = obj_atr['description']
            elif jhook.get('evet_type', None) == "note":
                embed.title = "This is a note..."
            elif jhook.get('object_kind', None) == "pipeline":
                embed.title = "Pipeline: ***{0}*** in ***{1}***".format(
                    jhook['object_attributes']['status'],
                    project['path_with_namespace']
                )
                embed.description = "Commit: [{0}]({1})".format(
                    jhook['commit']['id'][:8],
                    jhook['commit']['url']
                )
                for build in jhook['builds']:
                    embed.add_field(name=build['name'], value=build['status'])
            else:
                # embed.title = "{user_name} {event_name}".format(**jhook) + project['path_with_namespace']
                embed.title = "***WIP** hope mardown works here lol"

            await bot.get_channel(channel_id).send(embed=embed)
        elif hook.get('type', None) == "email":
            embed = discord.Embed()

            icon_url = bot.user.avatar_url
            embed.set_author(name=hook.get('name', 'Email'),
                             icon_url=icon_url)
            embed.title = jhook['subject']
            body = jhook['body']
            if len(body) > 1000:
                body = body[:1000] + "..."
            embed.description = "Sent by: **{0}**\n\n{1}".format(
                jhook['sender'],
                body
            )
            embed.url = jhook['url']
            embed.timestamp = datetime.datetime.fromisoformat(jhook['date'])
        else:
            text = "This webhook type is not supported!"
            # Debugging
            # if len(text) > 2000:
            #     with open("/files/output", "a") as ofile:
            #         ofile.write(text)
            #     text = "Text was too long... saved into output file for debugging\n\n"
            await bot.get_channel(channel_id).send(text)
        return json_response({"success": "true"}, status=200, content_type='application/json')
    else:
        return json_response({"success": "false"}, status=404, content_type='application/json')

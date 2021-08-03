import discord
from discord.ext import commands
from aiohttp.web import json_response
from typing import Optional, Union

from core.database.schemas import (
    PartyCreateWebhook,
    MemberJoinWebhook,
    PartyFullWebhook,
    PartyReadyWebhook,
    PartyTimedoutWebhook,
)

from core.config import settings
from core.utils import discord_avatar_url


async def parse_webhook(
    data: dict,
) -> Optional[
    Union[
        PartyCreateWebhook,
        MemberJoinWebhook,
        PartyFullWebhook,
        PartyReadyWebhook,
        PartyTimedoutWebhook,
    ]
]:
    """
    Parse event from data

    :param data: dict
    :return: Event object
    """
    if data.get("event").get("name") == "on_party_create":
        return PartyCreateWebhook.parse_obj(data)
    elif data.get("event").get("name") == "on_member_join":
        return MemberJoinWebhook.parse_obj(data)
    elif data.get("event").get("name") == "on_party_full":
        return PartyFullWebhook.parse_obj(data)
    elif data.get("event").get("name") == "on_party_ready":
        return PartyReadyWebhook.parse_obj(data)
    elif data.get("event").get("name") == "on_party_timed_out":
        return PartyTimedoutWebhook.parse_obj(data)
    else:
        return None


class Parser:
    def __init__(self, bot: commands.Bot):
        """
        Parser constructor

        :param bot:
        """
        self.__bot = bot
        self.__embed = discord.Embed()
        self.__channel_id = None

    async def on_party_create(self, event: PartyCreateWebhook):
        """
        Assemble on_party_create message.

        :param event: Event object
        :return:
        """
        self.__channel_id = int(event.party.channel.discord_id)

        self.__embed.set_author(
            name=event.party.leader.name,
            icon_url=discord_avatar_url(
                event.party.leader, support_gifs=True, size=4096
            ),
            url=settings.SITE_HOSTNAME,
        )

        self.__embed.title = f"***{event.party.leader.name}*** is looking for more players to play ***{event.party.game.name}***!"

        # Cut description if too long
        if len(event.party.description) > 1000:
            event.party.description = event.party.description[:1000] + "..."

        self.__embed.description = (
            f"**{event.party.title}**\n"
            f"{event.party.description}\n"
            f"[Join here!]({settings.SITE_HOSTNAME}/#/parties/{event.party.id})"
        )
        self.__embed.add_field(
            name="Players",
            value=f"{len(event.party.members)}/{event.party.max_players}",
        )

        if event.party.end_time and event.party.start_time:
            duration = event.party.end_time - event.party.start_time
            total_sec = duration.total_seconds()

            # Duration to strings
            dh = int(total_sec // (60 * 60))
            dm = int((total_sec % (60 * 60)) // 60)
            ds = int((total_sec % (60 * 60)) % 60)
            str_duration = f"{dh:02}:{dm:02}:{ds:02}"
            self.__embed.add_field(name="Duration", value="{0}".format(str_duration))

    async def on_member_join(self, event: MemberJoinWebhook):
        """
        Assemble on_member_join message.

        :param event: Event object
        :return:
        """
        self.__channel_id = int(event.channel.discord_id)

        self.__embed.set_author(
            name=event.member.player.name,
            icon_url=discord_avatar_url(
                event.member.player, support_gifs=True, size=4096
            ),
            url=settings.SITE_HOSTNAME,
        )

        self.__embed.title = (
            f"**{event.member.player.name}** " f"joined **{event.member.party.title}**!"
        )

        self.__embed.add_field(
            name="Players",
            value=f"{len(event.member.party.members)}/"
            f"{event.member.party.max_players}",
        )

    async def on_party_full(self, event: PartyFullWebhook):
        """
        Assemble on_party_full message.

        :param event: Event object
        :return:
        """
        self.__channel_id = int(event.party.channel.discord_id)

        self.__embed.set_author(
            name=event.party.leader.name,
            icon_url=discord_avatar_url(
                event.party.leader, support_gifs=True, size=4096
            ),
            url=settings.SITE_HOSTNAME,
        )

        self.__embed.title = f"**{event.party.title}** is full!"

        self.__embed.description = "**Players**:"

        for member in event.party.members:
            self.__embed.add_field(
                name=member.player.name,
                value=member.role.name if member.role else "",
                inline=False,
            )

    async def on_party_ready(self, event: PartyReadyWebhook):
        """
        Assemble on_party_ready message.

        :param event: Event object
        :return:
        """
        self.__channel_id = int(event.party.channel.discord_id)

        self.__embed.set_author(
            name=event.party.leader.name,
            icon_url=discord_avatar_url(
                event.party.leader, support_gifs=True, size=4096
            ),
            url=settings.SITE_HOSTNAME,
        )

        self.__embed.title = f"**{event.party.title}** is ready!"

        self.__embed.description = (
            "Party minimum required players reached!\n\n**Players**:"
        )

        for member in event.party.members:
            self.__embed.add_field(
                name=member.player.name,
                value=member.role.name if member.role else "",
                inline=False,
            )

    async def on_party_timed_out(self, event: PartyTimedoutWebhook):
        """
        Assemble on_party_timed_out message.

        :param event: Event object
        :return:
        """
        self.__channel_id = int(event.party.channel.discord_id)

        self.__embed.set_author(
            name=event.party.leader.name,
            icon_url=discord_avatar_url(
                event.party.leader, support_gifs=True, size=4096
            ),
            url=settings.SITE_HOSTNAME,
        )

        self.__embed.title = f"**{event.party.title}** timed out! :/"

        self.__embed.description = f"\n\n**Players**:"

        for member in event.party.members:
            if member.role and event.party.leader_id == member.player_id:
                member_value = f"Leader - {member.role.name}"
            elif event.party.leader_id == member.player_id:
                member_value = "Leader"
            elif member.role:
                member_value = f"Member - {member.role.name}"
            else:
                member_value = "Member"

            self.__embed.add_field(
                name=member.player.name,
                value=member_value,
                inline=False,
            )

    async def parse(self, data: dict):
        """
        Parse data and send message accordingly

        :param data: Received data
        :return:
        """

        self.__embed.set_author(
            name="PartyFiller",
            icon_url=self.__bot.user.avatar_url,
            url=settings.SITE_HOSTNAME,
        )

        hook = await parse_webhook(data)

        if hook is None:
            return json_response(
                {"error": "Unknown webhook event!"},
                status=400,
                content_type="application/json",
            )

        if hook.event.name == "on_party_create":
            await self.on_party_create(hook)
        elif hook.event.name == "on_member_join":
            await self.on_member_join(hook)
        elif hook.event.name == "on_party_full":
            await self.on_party_full(hook)
        elif hook.event.name == "on_party_ready":
            await self.on_party_ready(hook)
        elif hook.event.name == "on_party_timed_out":
            await self.on_party_timed_out(hook)
        else:
            return json_response(
                {"error": "Unknown webhook event!"},
                status=400,
                content_type="application/json",
            )

        # Check that channel exists
        if self.__bot.get_channel(self.__channel_id) is None:
            raise ValueError("Bot cannot find channel!")

        # Send message
        await self.__bot.get_channel(self.__channel_id).send(embed=self.__embed)

        return json_response(
            {"success": "true"}, status=200, content_type="application/json"
        )

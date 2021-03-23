import discord
import datetime
from discord.ext import commands

from core.config import settings

from core.database import Session, session_lock
from core.database.models import Webhook

from core.tools import generate_identity

from sqlalchemy import select


class Webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(no_pm=True)
    async def webhook(self, ctx):
        """
        Webhook management
        :param ctx: Context
        :return:
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed()
            embed.set_author(name=self.bot.user.name,
                             url=settings.SITE_HOSTNAME,
                             icon_url=self.bot.user.avatar_url)
            embed.title = "Invalid webhook command! `!help webhook` " \
                          "for more info"
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @webhook.command(pass_context=True, no_pm=True)
    async def add(self, ctx, name: str, channel_id: str):
        """
        Add webhook with given name and default destination channel
        :param ctx: Context
        :param name: Webhook name
        :param channel_id: Channel ID
        :return:
        """
        embed = discord.Embed()
        embed.set_author(name=self.bot.user.name,
                         url=settings.SITE_HOSTNAME,
                         icon_url=self.bot.user.avatar_url)
        async with session_lock:
            with Session() as db:
                identifier = None
                found = False

                # Generate new identifiers until a new one has been found
                while identifier is None or found:
                    identifier = generate_identity()

                    found = db.execute(
                        select(Webhook).where(Webhook.identifier == identifier)
                    ).scalars().first() is not None

                webhook = Webhook(
                    identifier=identifier,
                    name=name,
                    channel=channel_id,
                    server=str(ctx.guild.id)
                )

                db.add(webhook)
                db.commit()
                embed.colour = discord.Color.green()
                embed.title = "Webhook added!"
                embed.description = f"Webhook with identifier " \
                                    f"**{webhook.identifier}** added!"

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @webhook.command(pass_context=True, no_pm=True)
    async def remove(self, ctx, identifier: str):
        """
        Remove webhook with identifier
        :param ctx: Context
        :param identifier: Identifier of Webhook
        :return:
        """
        embed = discord.Embed()
        embed.set_author(name=self.bot.user.name,
                         url=settings.SITE_HOSTNAME,
                         icon_url=self.bot.user.avatar_url)
        async with session_lock:
            with Session() as db:
                webhook = db.execute(
                    select(Webhook).where(Webhook.identifier == identifier)
                ).scalars().first()

                if webhook is None:
                    embed.colour = discord.Color.red()
                    embed.title = "Webhook does not exist!"
                else:

                    db.delete(webhook)
                    db.commit()

                    embed.colour = discord.Color.green()
                    embed.title = "Webhook removed!"
                    embed.description = f"Webhook with identifier " \
                                        f"**{webhook.identifier}** removed!"

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @webhook.command(pass_context=True, no_pm=True)
    async def list(self, ctx):
        """
        List all webhooks on this server
        :param ctx: Context
        :return:
        """
        embed = discord.Embed()
        embed.set_author(name=self.bot.user.name,
                         url=settings.SITE_HOSTNAME,
                         icon_url=self.bot.user.avatar_url)
        async with session_lock:
            with Session() as db:
                webhooks = db.execute(
                    select(Webhook).where(Webhook.server == str(ctx.guild.id))
                ).scalars().All()

                embed.colour = discord.Color.green()
                embed.title = "Webhooks on this server..."
                for webhook in webhooks:
                    embed.add_field(
                        name=webhook.name,
                        value=webhook.identifier,
                        inline=False
                    )

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @webhook.command(pass_context=True, no_pm=True)
    async def edit(self, ctx, identifier: str, name: str = None, channel_id: str = None):
        """
        Edit webhook with identifier
        :param ctx: Context
        :param identifier: Identifier of webhook
        :param name: New name
        :param channel_id: New channel id
        :return:
        """
        embed = discord.Embed()
        embed.set_author(name=self.bot.user.name,
                         url=settings.SITE_HOSTNAME,
                         icon_url=self.bot.user.avatar_url)
        async with session_lock:
            with Session() as db:
                webhook = db.execute(
                    select(Webhook).where(Webhook.identifier == identifier)
                ).scalars().first()

                if name is not None:
                    webhook.name = name

                if channel_id is not None:
                    webhook.channel = channel_id

                db.add(webhook)
                db.commit()

                embed.colour = discord.Color.green()
                embed.title = "Webhook updated!"

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

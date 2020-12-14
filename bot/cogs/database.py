import discord
import datetime
import asyncio
import logging
from discord.ext import commands, tasks


class DatabaseCog(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name="database", hidden=True)
    @commands.is_owner()
    async def database_cmd(self, ctx, *args):
        embed = discord.Embed()
        message = ""
        if len(args) > 0:
            if args[0] == "setup":
                result = self.db.setup()
                message = "**Status**: {status}\n" \
                          "**Errors**: {errors}\n" \
                          "**Tables exist**: {tables_exist}".format(**result)
            elif args[0] == "update":
                result = self.db.update()
                message = "**Status**: {status}\n" \
                          "**Errors**: {errors}".format(**result)
            else:
                message = "Unknown arguments..."
        else:
            message = "Available subcommands: setup"
            embed.colour = discord.Color.red()

        embed.title = message
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

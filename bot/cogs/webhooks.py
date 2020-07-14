import discord
import datetime
import asyncio
from discord.ext import commands, tasks


class Webhooks(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name="webhook")
    async def webhook_cmd(self, ctx, *args):
        embed = discord.Embed()
        if len(args) > 0:
            if args[0] == "add":
                if len(args) > 1:
                    if len(args) > 4:
                        whook = {
                            "name": str(args[1]),
                            "channel": int(args[2]),
                            "type": str(args[3]),
                            "icon_url": str(args[4])
                        }
                    elif len(args) == 4:
                        whook = {
                            "name": str(args[1]),
                            "channel": int(args[2]),
                            "type": str(args[3]),
                        }
                    elif len(args) == 3:
                        whook = {
                            "name": str(args[1]),
                            "channel": int(args[2]),
                            "type": "other",
                        }
                    else:
                        whook = {
                            "name": str(args[1]),
                            "channel": ctx.channel.id,
                            "type": "other"
                        }
                    ide = self.db.add_webhook(webhook=whook)

                    # Final error checking
                    if ide.startswith("ERROR: "):
                        message = str(ide)
                        embed.colour = discord.Color.red()
                    else:
                        message = "Webhook '" + str(ide) + "' added."
                        embed.colour = discord.Color.green()
                else:
                    message = "Not enough arguments! (name, [channel_id], [type], [icon_url])"
                    embed.colour = discord.Color.red()
            elif args[0] == "remove":
                if self.db.remove_webhook(ide=args[1])['status'] == "success":
                    message = "Webhook '" + args[1] + "' removed."
                    embed.colour = discord.Color.green()
                else:
                    message = "Webhook '" + args[1] + "' doesn't exist."
                    embed.colour = discord.Color.red()
            elif args[0] == "list":
                webhooks = self.db.get_all_webhooks()
                if webhooks['status'] == "success":
                    message = "All webhooks"
                    for webhook in webhooks['webhooks']:
                        embed.add_field(
                            name=webhook['name'],
                            value="Type: {type}\nIdentifier: {identifier}".format(**webhook),
                            inline=False
                        )
                else:
                    message = "Error!"
                    embed.description = webhooks['status']
                    embed.colour = discord.Color.red()

            elif args[0] == "edit":
                message = "Work in progress..."
                embed.colour = discord.Color.orange()
            else:
                message = "Unknown arguments..."
                embed.colour = discord.Color.red()
        else:
            message = "Available subcommands: service, add, remove, edit"
            embed.colour = discord.Color.red()

        embed.title = message
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

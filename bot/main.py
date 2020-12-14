import asyncio
import logging
import os
from discord.ext import commands
from aiohttp.web import AppRunner, Application, TCPSite


from utils.database import Database
from utils.api import routes

from cogs.webhooks import Webhooks
from cogs.database import DatabaseCog


class Shutdown(Exception):
    pass


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
# handler = logging.FileHandler(filename='files/discord.log', encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

running = True

cogs = ['cogs.webhooks', 'cogs.database']


def main():

    print("Starting Bot...")

    token = os.environ.get("TOKEN", None)
    if token is None:
        print("Token not found!")
        return

    db_name = os.environ.get("DB_NAME", None)
    if db_name is None:
        print("Database name not found!")
        return

    db_user = os.environ.get("DB_USER", None)
    if db_user is None:
        print("Database user not found!")
        return

    db_pass = os.environ.get("DB_PASS", None)
    if db_pass is None:
        print("Database password not found!")
        return

    db = Database(db_name, db_user, db_pass)

    description = '''Semi-basic discord bot with webhooks'''
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or('!'),
        description=description,
        owner_id=128914478178762753
    )

    bot.add_cog(Webhooks(bot, db))
    bot.add_cog(DatabaseCog(bot, db))

    @bot.event
    async def on_ready():
        print("\nLogged in as:\n{0} (ID: {0.id})".format(bot.user))

        app = Application()
        app.add_routes(routes)

        # Pass bot and database to webserver
        app['bot'] = bot
        app['db'] = db

        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, '0.0.0.0', 9080)
        await site.start()

    loop = asyncio.get_event_loop()

    global running
    while running:
        try:
            async def login_task():
                await bot.login(token)
                await bot.connect()

            loop.run_until_complete(login_task())

        except Shutdown or KeyboardInterrupt:
            for task in asyncio.Task.all_tasks():
                task.cancel()

            loop.run_until_complete(bot.logout())

        finally:
            loop.close()

            running = False


if __name__ == '__main__':
    main()

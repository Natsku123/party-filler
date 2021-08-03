import signal
import discord
from discord.ext import commands
from aiohttp.web import AppRunner, Application, TCPSite

from core.api import routes


from core.config import settings, logger


def main():

    logger.info("Starting bot...")

    description = """PartyFiller-bot, I will fill your parties!"""

    intents = discord.Intents.default()

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!"),
        description=description,
        # TODO make dynamic
        owner_id=128914478178762753,
        intents=intents,
    )

    @bot.event
    async def on_ready():
        logger.info("\nLogged in as:\n{0} (ID: {0.id})".format(bot.user))

        app = Application()
        app.add_routes(routes)

        # Pass bot to webserver
        app["bot"] = bot

        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, "0.0.0.0", 9080)
        await site.start()

    def handle_sigterm(sig, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, handle_sigterm)

    bot.run(settings.TOKEN)


if __name__ == "__main__":
    main()

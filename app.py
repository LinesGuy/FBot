from statistics import multimode
from discord.ext import commands
import discord
import logging
import datetime
import json
import os
import mysql.connector


class Bot(commands.AutoShardedBot):
    def __init__(self):
        logging.info("Session started!")

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix="fbot ", intents=intents, chunk_guilds_at_startup=False
        )

    async def setup_hook(self):
        logger = logging.getLogger("discord")
        logger.info("setup_hook() called")

        self.remove_command("help")
        # TODO load entire folder
        for extension in [
            "hello",
            "ping",
            "extension_handler",
            "error_handler",
            "trigger_response",
            "help",
            "eval",
            "set_presence",
            "ppsize",
        ]:
            logger.info(f"Loading extension: {extension}")
            await self.load_extension(f"extensions.{extension}")

        logger.info(f"Done loading extensions")

        await self.connect_db()

    async def connect_db(self):
        self.db = mysql.connector.connect(
        host=self.settings["database"]["host"],
        user=self.settings["database"]["user"],
        password=self.settings["database"]["password"],
        database=self.settings["database"]["database_name"],
        autocommit=True
    )
    async def on_shard_resumed(self, shard_id):
        await self.connect_db()

    async def on_ready(self):
        logging.getLogger("discord").info("on_ready() called")
        await self.change_presence(
            status=discord.Status.online, activity=discord.Game(name="soontm?")
        )
        await self.get_channel(1100477664617312386).send("Bot is ready!")

def main():
    # Set up logging
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    # Write log to file
    fileHandler = logging.FileHandler(
        os.path.join("Logs", datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))
    )
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    # Write log to console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    logger.propagate = False  # Supresses default log format
    logger.info("Set up logging")

    bot = Bot()
    bot.settings = json.load(open("settings.json", "r"))
    bot.owner_ids = set(bot.settings["owner_ids"])
    bot.run(bot.settings["tokens"]["lines"], log_handler=None)


if __name__ == "__main__":
    main()

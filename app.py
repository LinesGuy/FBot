from discord.ext import commands
import discord
import logging
import datetime
import json
import os

class Bot(commands.AutoShardedBot):
    def __init__(self):
        logging.info("Session started!")

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix="fbot ", intents=intents, chunk_guilds_at_startup=False)

        # TODO database shit
        # TODO trigger/response shit
        # TODO replace default help command with fbot help
        # TODO load cogs
        #for cog in fn.getcogs():
        #    if cog not in []:
        #        print(f"\nLoading {cog}...", end="")
        #        try: await self.reload_extension("cogs." + cog[:-3])
        #        except: await self.load_extension("cogs." + cog[:-3])
        #        finally: print("Done", end="")
        #print("\n\n > Loaded cogs\n")
    async def setup_hook(self):
        logger = logging.getLogger("discord")
        logger.info("setup_hook() called")
        for extension in ["hello", "ping", "extension_handler", "error_handler"]:
            logger.info(f"Loading extension: {extension}")
            await self.load_extension(f"extensions.{extension}")
        logger.info(f"Done loading extensions")

    async def on_ready(self):
        logging.getLogger("discord").info("on_ready() called")
        await self.change_presence(status=discord.Status.idle, activity=discord.Game(name="zzz"))
        await self.get_channel(1100477664617312386).send("Bot is ready!")

    def embed(self, user, title, *desc, url=""):
        colour = self.get_colour(user.id)
        desc = "\n".join(desc)
        return discord.Embed(title=title, description=desc, colour=colour, url=url)

    def predicate(self, ctx):

        user = ctx.author.id
        command = ctx.command.name

        if not self.ready():
            return

        if command in cm.devcmds:
            if user not in self.devs:
                raise commands.NotOwner()

        if str(ctx.channel.type) != "private":
            bot_perms = ctx.channel.permissions_for(ctx.guild.get_member(self.user.id))

            valid, perms = [], {}
            for perm in cm.perms[command]:
                if not perm.startswith("("):
                    bot_perm = getattr(bot_perms, perm)
                else: bot_perm = True
                valid.append(bot_perm)
                perms[perm] = bot_perm

            if not all(valid):
                page = "**Missing Permissions**\n\n"
                for perm in perms:
                    if perm.startswith("("):
                        perms[perm] = getattr(bot_perms, perm[1:-1])
                    page += f"{fn.emojis[perms[perm]]} ~ {fn.formatperm(perm)}\n"
                raise commands.CheckFailure(message=page)
        else:
            if cm.commands[command][5] == "*Yes*":
                raise commands.NoPrivateMessage()

        cooldown = self.cache.cooldowns.get(user, command)
        if cooldown:
            self.stats.commands_ratelimited += 1
            raise commands.CommandOnCooldown(commands.BucketType.user, cooldown)
        self.stats.commands_processed += 1
        return True

def main():
    # Set up logging
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fileHandler = logging.FileHandler(os.path.join("Logs", datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")))
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    logger.propagate = False
    logger.info("Set up logging")

    # Load settings
    settings = json.load(open("settings.json", "r"))

    # It's showtime, baby!
    bot = Bot()
    bot.run(settings["tokens"]["lines"], log_handler=None)

if __name__ == "__main__":
    main()
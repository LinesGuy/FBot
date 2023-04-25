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

        self.startup()
        # TODO database shit
        # TODO trigger/response shit
        # TODO replace default help command with fbot help

        for cog in fn.getcogs():
            if cog not in []:
                print(f"\nLoading {cog}...", end="")
                try: await self.reload_extension("cogs." + cog[:-3])
                except: await self.load_extension("cogs." + cog[:-3])
                finally: print("Done", end="")
        print("\n\n > Loaded cogs\n")

        self.premium = await self.get_premium()
        self.cache = cache.Cache(self.settings.devs, self.premium)

        for command in cm.commands:
            self.cache.cooldowns.add(command, tuple(cm.commands[command][3:5]))
        for command in cm.devcmds:
            self.cache.cooldowns.add(command, (0, 0))
        print(" > Finished setting up cooldowns")

        await self.change_presence(status=discord.Status.online,
                                activity=discord.Game(name="'FBot help'"))

        self.prepped = True

    async def cleanup(self):
        c = await self.db.connection(autoclose=False)
        guild_ids = dict()
        for guild in bot.guilds:
            guild_ids[guild.id] = guild

        count = [0, 0]
        for guild in bot.guilds:
            await c.execute("SELECT guild_id FROM guilds WHERE guild_id=%s;", (guild.id,))
            if not await c.fetchone():
                await self.db.addguild(guild.id)
                count[0] += 1
            # doesnt work for some god foresaken reason
            await c.execute("SELECT guild_id FROM counting WHERE guild_id=%s;", (guild.id,))
            result = await c.fetchone()
            if not result:
                await self.db.addcounting(guild.id)
                count[1] += 1
        print("Added", count[0], "guilds to 'guilds'")
        print("Added", count[1], "missing guilds to 'counting'")

        count = [0, 0]
        await c.execute("SELECT guild_id FROM guilds;")
        for row in await c.fetchall():
            guild_id = row[0]
            if not (guild_id in guild_ids):
                await self.db.removeguild(guild_id)
                count[0] += 1
            else:
                channel_ids = [channel.id for channel in guild_ids[guild_id].channels]
                await c.execute("SELECT channel_id FROM channels WHERE guild_id=%s;", (guild_id,))
                for row in await c.fetchall():
                    channel_id = row[0]
                    if not (channel_id in channel_ids):
                        await c.execute("DELETE FROM channels WHERE channel_id=%s;", (channel_id,))
                        count[1] += 1
        print("Removed", count[0], "guilds from 'guilds'")
        print("Removed", count[1], "channels from 'channels'")

        count = 0
        await c.execute("SELECT guild_id FROM channels;")
        for row in await c.fetchall():
            guild_id = row[0]
            if not (guild_id in guild_ids):
                await c.execute("DELETE FROM channels WHERE guild_id=%s;", (guild_id,))
                count += 1
        print("Removed", count, "guild channels from 'channels'")

        count = 0
        await c.execute("SELECT guild_id FROM counting;")
        for row in await c.fetchall():
            guild_id = row[0]
            if not (guild_id in guild_ids):
                await c.execute("DELETE FROM counting WHERE guild_id=%s;", (guild_id,))
                count += 1
        print("Removed", count, "guilds from 'counting'\n")

        await c.close()

        self.cleaning = False
        print(f" > Bot is ready")
        self.dispatch("bot_ready")
        self.bot_ready = True

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
    # Hai :3
    print("Hello, world!")

    # Set up logging
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("discord.http").setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fileHandler = logging.FileHandler(os.path.join("Logs", datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")))
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # Load settings
    settings = json.load(open("settings.json", "r"))

    # It's showtime, baby!
    bot = Bot()
    bot.run(settings["tokens"]["main"], log_level=logging.INFO)

if __name__ == "__main__":
    main()
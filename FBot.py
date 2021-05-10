import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
import discord
import dbl
import sys
import os
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, "lib")
from functions import fn, ftime, voting_handler, predicate
from database import db
from triggers import tr
from commands import cmds

import commands as cm

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

fn = fn()

owners = [671791003065384987, 216260005827969024, 311178459919417344]

class FBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=fn.getprefix,owner_ids=owners, intents=intents)
        self.dbl = dbl.DBLClient(self, os.getenv("TOPGG_TOKEN"), webhook_path="/dblwebhook",
            webhook_auth=os.getenv("WEBHOOK_AUTH"), webhook_port=6000)

        self.fn = fn
        self.db = db()

        tr.load()
        cmds.load()

        self.ftime = ftime()

    async def on_connect(self):
        print(f"\n > Began signing into Discord as {self.user}")

    async def on_ready(self):
        print(f" > Finished signing into Discord as {self.user}\n")
        self.db.Check_Guilds(self.guilds)
        fn.setbot(self)
        self.ftime.set()

        self.remove_command("help")
        for cog in self.fn.getcogs():
            if cog not in ["image.py"]: # Cogs not to load
                print(f"Loading {cog}...", end="")
                try: self.reload_extension("cogs." + cog[:-3])
                except: self.load_extension("cogs." + cog[:-3])
                finally: print("Done")
        print("\n > Finished loading cogs")

        for command in cm.commands:
            self.cache["Cooldowns"].add_command(command, tuple(cm.commands[command][3:5]))
        for command in cm.devcmds:
            self.cache["Cooldowns"].add_command(command, (0, 0))
        print(" > Finished setting up cooldowns\n")
        
        await self.change_presence(status=discord.Status.online,
                                activity=discord.Game(name="'FBot help'"))


bot = FBot()
voting_handler(bot)

print(f" > Session started at {bot.ftime.start}")
token = os.getenv("JUDE_TOKEN") # 1 for FBot, 2 for Jude, 3 for Chris

@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")
    bot.db.Check_Guilds(bot.guilds)
    fn.setbot(bot)

    bot.remove_command("help")
    for cog in bot.fn.getcogs():
        if cog not in []: # Cogs not to load
            print(f"Loading {cog}...", end="")
            try: bot.reload_extension("cogs." + cog[:-3])
            except: bot.load_extension("cogs." + cog[:-3])
            finally: print("Done")
    print("\n > Finished loading cogs")

    for command in cm.commands:
        bot.cache["Cooldowns"].add_command(command, tuple(cm.commands[command][3:5]))
    for command in cm.devcmds:
        bot.cache["Cooldowns"].add_command(command, (0, 0))
    print(" > Finished setting up cooldowns\n")
       
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="'FBot help'"))
bot.add_check(predicate)
bot.run(token)
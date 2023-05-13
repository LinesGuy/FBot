from discord.ext import commands
import csv
import random

responses = [
    "Someone has bad taste in photos",
    "Your right to live has now been revoked",
    "I wish I hadn't seen that",
    "MY EYES! MY EYES! WHY WOULD YOU SEND THAT!?",
    "Oh my, what have I just witnessed",
    "That be kinda stanky ngl",
    "Spare me, please",
    "I'm not feeling that, delete immediatley",
    "That is not vibe",
]

funnies = [
    "Hmm, maybe I'll laugh too next time",
    "HAHAHA, was that the reaction you were looking for?",
    "It would be easier to laugh if it were funny",
    "That is **h i l a r i o u s**",
    "L O L",
    "Wow my dude that is so funny",
]

answers = [
    "Good question",
    "idk",
    "Why are you asking me?",
    "I don't think we'll ever know",
]

WHOLE = 0  # Entire message must match trigger
START = 1  # Message must start with trigger
END = 2  # Message must end with trigger
ANYWHERE = 3  # Message must contain trigger anywhere in the message
REPEAT = 4  # Message starts and ends with some trigger with any amount of a repeated letter between
LETTERS = 5  # Message must consist entirely of the trigger repeated (e.g oooooo, hehehe, aaaaa)
REPLACE = 6  # Message must contain trigger, which will be replaced by the response

trigger_types = ["whole", "start", "end", "anywhere", "repeat", "letters", "replace"]

EXACT = 0
ANYCASE = 1

cases = ["exact", "anycase"]

entries = list()


class entry:
    def __init__(self, _triggers, _type, _case, _response, _priority):
        self.triggers = _triggers
        self.type = trigger_types.index(_type)
        self.case = cases.index(_case)
        if self.case == ANYCASE:
            self.triggers = [t.lower() for t in self.triggers]
        self.response = _response
        self.priority = _priority


for row in csv.reader(open("data/CSVs/Triggers.csv", "r")):
    entries.append(entry(row[0].split("\\"), *row[1:]))


class TriggerResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't respond to bots (including self)
        if message.author.bot:
            return
        # If user is executing a command, don't treat it as a trigger
        if (
            message.content.startswith("fbot ")
            and message.content.split(" ")[1] in self.bot.all_commands.keys()
        ):
            return
        # Check if FBot is enabled in the server
        c = self.bot.db.cursor()
        c.execute("SELECT Enabled FROM Guild WHERE id=%s;", (message.guild.id,))
        enabled = c.fetchone()
        if enabled is None:
            # Oopsie! Server isn't in DB. Let's add it, and enable it by default.
            enabled = (1,)
            c.execute(
                "INSERT INTO Guild (id, Enabled) VALUES (%s, %s);",
                (message.guild.id, 1),
            )
        if not enabled[0]:
            return
        # TODO fball
        # TODO respond to "f bot", self.bot.user.id etc with fbot help
        # TODO respond to attachments
        # TODO implement priorities
        # TODO if response length greater than 2000, trim to first 1997 chars and add ...
        for entry in entries:
            msg = message.content.lower() if entry.case == ANYCASE else message.content
            for alias in entry.triggers:
                # All these trigger types are all trivially checked
                if (
                    (entry.type == WHOLE and msg == alias)
                    or (entry.type == START and msg.startswith(alias))
                    or (entry.type == END and msg.endswith(alias))
                    or (entry.type == ANYWHERE and alias in msg)
                    or (entry.type == LETTERS and msg.replace(alias, "") == "")
                    or (entry.type == REPLACE and alias in msg)
                ):
                    break
                # The REPLACE type requires a bit more code:
                if entry.type == REPEAT:
                    for alias in entry.triggers:
                        start, end = alias.split("~")
                        letter = start[-1]
                        if (
                            msg.startswith(start)
                            and msg.endswith(end)
                            and (
                                all([c == letter for c in msg[len(start) : -len(end)]])
                            )
                        ):
                            trigger = trigger
                            break
                    else:
                        continue
                    break
            else:
            return  # No response
        if entry.type == REPLACE:
            response = message.content.replace(alias, entry.response)
        else:
            response = entry.response
        response = response.replace("{username}", message.author.display_name)
        response = response.replace("{answer}", random.choice(answers))
        response = response.replace("{funny}", random.choice(funnies))
        response = response.replace("{message}", message.content)
        response = response.replace("{after}", message.content[len(alias) :])
        await message.channel.send(response)

    @commands.command()
    async def on(self, ctx):
        c = self.bot.db.cursor()
        c.execute("SELECT * FROM Guild WHERE id=%s", (ctx.guild.id,))
        if c.fetchone() is None:
            c.execute("INSERT INTO Guild (id, Enabled) VALUES (%s, 1)", (ctx.guild.id,))
        else:
            c.execute("UPDATE Guild SET Enabled = 1 WHERE id=%s;", (ctx.guild.id,))
        await ctx.reply("Enabled")

    @commands.command()
    async def off(self, ctx):
        c = self.bot.db.cursor()
        c.execute("SELECT * FROM Guild WHERE id=%s", (ctx.guild.id,))
        if c.fetchone() is None:
            c.execute("INSERT INTO Guild (id, Enabled) VALUES (%s, 0)", (ctx.guild.id,))
        else:
            c.execute("UPDATE Guild SET Enabled = 0 WHERE id=%s;", (ctx.guild.id,))
        await ctx.reply("Disabled")


async def setup(bot):
    await bot.add_cog(TriggerResponse(bot))
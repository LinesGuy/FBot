from discord.ext import commands

class TriggerResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't respond to bots (including self)
        if message.author.bot:
            return
        # If user is executing a command, don't treat it as a trigger
        if message.content.split(' ')[0] in self.bot.all_commands:
            return
        # TODO fball
        # TODO respond to "f bot", self.bot.user.id etc with fbot help
        # TODO respond to attachments
        # TODO implement trigger response lol
        # TODO if response length greater than 2000, trim to first 1997 chars and add ...

async def setup(bot):
    await bot.add_cog(TriggerResponse(bot))
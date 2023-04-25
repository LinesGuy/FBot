from discord.ext import commands

class Errorhandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        match type(error):
            case commands.NotOwner:
                await ctx.reply("Only bot owners can run this command!")

async def setup(bot):
    await bot.add_cog(Errorhandler(bot))
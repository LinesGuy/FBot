import traceback
from discord.ext import commands

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, content):
        try:
            result = str(eval(content))
        except Exception as e:
            result = "".join(traceback.format_exception(e, e, e.__traceback__))
        await ctx.send(f"```{result}```")

async def setup(bot):
    await bot.add_cog(Eval(bot))
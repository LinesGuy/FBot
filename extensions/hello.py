from discord.ext import commands

class SampleExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(SampleExtension(bot))

async def teardown(bot):
    pass
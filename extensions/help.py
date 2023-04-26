from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send("soontm, use `fbot commands` for now")

    @commands.command()
    async def commands(self, ctx):
        await ctx.send("```" + "\n".join(list(self.bot.all_commands.keys())) + "```")


async def setup(bot):
    await bot.add_cog(Help(bot))


async def teardown(bot):
    pass
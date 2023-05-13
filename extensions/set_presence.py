from discord.ext import commands
import discord

class SetPresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Sets the current presence of the bot", brief="Sets bot presence", usage="fbot presence <awesome presence>")
    async def presence(self, ctx, *, content):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name=content))
        await ctx.reply("Updated presence")

async def setup(bot):
    await bot.add_cog(SetPresence(bot))

async def teardown(bot):
    pass




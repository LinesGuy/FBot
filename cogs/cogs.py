from discord.ext import commands
from discord import Embed

class Cogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def unload(self, ctx, cog):
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                if cog != "cogs":
                    try: await self.bot.unload_extension("cogs." + cog)
                    except: unable.append(cog)
            embed = self.bot.embed(ctx.author, "FBot cogs",
                             "Unloaded all cogs" + format_unable(unable))
        else:
            try:
                await self.bot.unload_extension("cogs." + cog)
                embed = self.bot.embed(ctx.author, "FBot cogs",
                                 f"Unloaded cog: `{cog}`")
            except Exception as e:
                embed = errorembed(f"Failed to unload cog: {cog}", str(e))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cogs(bot))
from discord.ext import commands
import logging
import os

class ExtensionHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        logger = logging.getLogger("discord")
        path = os.path.join("extensions", f"{extension}.py")
        if not os.path.isfile(path):
            await ctx.reply(f"File not found: {path}")
            return
        if f"extensions.{extension}" in self.bot.extensions.keys():
            await ctx.reply(f"Extension {extension} is already loaded!")
            return
        logger.info(f"Loading extension: {extension}")
        await self.bot.load_extension(f"extensions.{extension}")
        await ctx.send(f"Loaded extension: {extension}")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        path = os.path.join("extensions", f"{extension}.py")
        if not os.path.isfile(path):
            await ctx.reply(f"File not found: {path}")
            return
        if f"extensions.{extension}" not in self.bot.extensions.keys():
            await ctx.reply(f"Extension {extension} isn't loaded!")
            return
        await self.bot.reload_extension(f"extensions.{extension}")
        await ctx.send(f"Reloaded extension: {extension}")

    @commands.command()
    @commands.is_owner()
    async def extensions(self, ctx):
        await ctx.send("```" + '\n'.join(list(self.bot.extensions.keys())) + "```")

    @commands.command()
    @commands.is_owner()
    async def cogs(self, ctx):
        await ctx.send("```" + '\n'.join(list(self.bot.cogs.keys())) + "```")

async def setup(bot):
    await bot.add_cog(ExtensionHandler(bot))
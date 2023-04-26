from traceback import format_exception
from discord.ext import commands

class Errorhandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        match type(error):
            case commands.CommandNotFound:
                return
            case commands.NotOwner:
                await ctx.reply("Only bot owners can run this command!")
            case _:
                await ctx.send("An unusual error has occured, the devs have been notified.")

                error_msg  = f"Error on message: `{ctx.message.content}`\n"
                error_msg += f"Author: `{ctx.message.author}`\nid: `{ctx.message.author.id}`\n"
                error_msg += f"Guild: `{ctx.message.guild}`\nid: `{ctx.message.guild.id}`\n"
                error_msg += f"```{format_exception(error, error, error.__traceback__)}```"
                await self.bot.get_channel(727320090483359844).send(error_msg)


async def setup(bot):
    await bot.add_cog(Errorhandler(bot))
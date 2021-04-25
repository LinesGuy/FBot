from discord import AllowedMentions
from discord.ext import commands
from functions import predicate

class say(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="say")
    async def _Say(self, ctx, *inp):
        inp = " ".join(inp)
        if not inp == "":
            try: await ctx.message.delete()
            except: pass
            await ctx.send(inp + "ㅤ", allowed_mentions=AllowedMentions.none())
        else:
            await ctx.send("What do you want me to say!?")

def setup(bot):
    bot.add_cog(say(bot))
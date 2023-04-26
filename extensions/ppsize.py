from discord.ext import commands
import random


class ppsize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ppsize(self, ctx, target=None):
        if target is None:
            member = ctx.author
        else:
            member = await commands.MemberConverter().convert(ctx, target)
            if member is None:
                await ctx.reply("Command usage: `fbot ppsize` or `fbot ppsize <@user>`")
                return

        if member.bot:
            await ctx.reply("Bots don't have pps, you do know that?")
            return

        c = self.bot.db.cursor()
        c.execute("SELECT ppsize FROM User WHERE id=%s;", (member.id,))
        size = c.fetchone()
        if size is None:
            # User hasn't been assigned a ppsize yet, check if user exists at all:
            c.execute("SELECT * FROM User WHERE id = %s", (member.id,))
            if c.fetchone() is None:
                # Register new user
                c.execute("INSERT INTO User (id) VALUES (%s);", (member.id,))
            # Assign this user a random ppsize
            size = random.randint(1, 16)
            c.execute("UPDATE User SET ppsize = %s WHERE id = %s;", (size, member.id))
            self.bot.db.commit()
        else:
            size = size[0]
        await ctx.reply(f"{member.mention}'s ppsize: 8{'=' * size}D")
        pass

    @commands.command()
    async def setppsize(self, ctx, target, size: int):
        if size > 1950:
            await ctx.reply("That ppsize is too big to fit in a discord message. Max size is 1950")
        member = await commands.MemberConverter().convert(ctx, target)
        if member is None:
            await ctx.reply("Target not found. Command usage: `fbot setppsize <@user>`")
            return
        if member.bot:
            await ctx.reply("Can't set ppsize of a bot.")
            return
        c = self.bot.db.cursor()
        # Check if user exists
        c.execute("SELECT * FROM User WHERE id = %s", (member.id,))
        if c.fetchone() is None:
            # Register new user
            c.execute("INSERT INTO User (id) VALUES (%s);", (member.id,))
        c.execute("UPDATE User SET ppsize = %s WHERE id = %s;", (size, member.id))
        self.bot.db.commit()
        await ctx.reply("Updated ppsize succsesfully")



async def setup(bot):
    await bot.add_cog(ppsize(bot))
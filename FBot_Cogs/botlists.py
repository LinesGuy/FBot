from functions import cooldown, fn
from discord.ext import commands
import economy as e
import requests
import discord
import dbl

f = "~~f~~ "

class fakeuser: id = 0
user = fakeuser()

gettoken = fn().gettoken
bot_id = "711934102906994699"
bfdapi = f"https://botsfordiscord.com/api/bot/{bot_id}"
dbggapi = f"https://discord.bots.gg/api/v1/bots/{bot_id}/stats"
dblapi = f"https://discordbotlist.com/api/v1/bots/{bot_id}/stats"

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbl = bot.dbl
        self.voteschannel = self.bot.get_channel(757722305395949572).send

    @commands.command(name="scounts")
    @commands.is_owner()
    async def _SCOUNTS(self, ctx):
        servers = len(self.bot.guilds)
        embed = self.bot.fn.embed(ctx.author, f"Server Counts `{servers}`")
        msg = await ctx.send(embed=embed)

        # top.gg
        try:
            await self.dbl.post_guild_count()
            content = "**top.gg:** success"
            embed.description = content
        except:
            content = "**tog.gg:** failed"
            embed.description = content
        await msg.edit(embed=embed)

        # botsfordiscord.com
        data = {"server_count": servers}
        headers = {"Authorization": gettoken(6)}
        res = requests.post(bfdapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**botsfordiscord.com:** success"
            embed.description = content
        else:
            content += "\n**botsfordiscord.com:** failed"
            embed.description = content
        await msg.edit(embed=embed)

        # discord.bots.gg
        data = {"guildCount": servers}
        headers = {"Authorization": gettoken(7)}
        res = requests.post(dbggapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**discord.bots.gg:** success"
            embed.description = content
        else:
            content += "\n**discord.bots.gg:** failed"
            embed.description = content
        await msg.edit(embed=embed)

        # discordbotlist.com
        data = {"guilds": servers}
        headers = {"Authorization": gettoken(8)}
        res = requests.post(dblapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**discordbotlist.com:** success"
            embed.description = content
        else:
            content += "\n**discordbotlist.com:** failed"
            embed.description = content
        await msg.edit(embed=embed)

    @commands.command(name="vote")
    @commands.check(cooldown)
    async def _Vote(self, ctx):
        fn, db, ftime = self.bot.fn, self.bot.db, self.bot.ftime
        user = ctx.author
        job = db.getjob(user.id)
        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)
        salary = e.salaries[job] * jobmulti
        salary *= db.getusermulti(user.id)

        multi = 20
        if ftime.is_weekend(): multi *= 2
        
        embed = fn.embed(user, "FBot Vote",
                         "If you vote you'll earn your salary without tax",
                         f"So **~~f~~ {round(salary)}** if I'm not mistaken",
                         "AND multiplier worth {multi} messages!\n",

                         f"[top.gg vote]({fn.votetop})",
                         f"[botsfordiscord.com]({fn.votebfd})",
                         f"[discordbotlist.com]({fn.votedbl}) (No rewards)")
        await ctx.send(embed=embed)

    def vote_rewards(self, user_id):
        db = self.bot.db
        
        job = db.getjob(user_id)
        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user_id)
        salary = e.salaries[job] * jobmulti
        salary = round(salary * db.getusermulti(user_id))
        db.updatebal(user_id, salary)

        bonus = 1
        if self.bot.ftime.isweekend(): bonus = 2
        db.increasemultiplier(user_id, 0, 20 * bonus)

        return salary

    @commands.Cog.listener()
    async def on_vote(self, site, data):
        user_id = int(data["user"])
        self.bot.db.register(user_id)
        try: name = await self.bot.fetch_user(user_id).name
        except: name = "User"

        if data["type"] == "test":
            embed = self.bot.fn.embed(user, site + " test",
                    f"{name} tested out the webhook")
        elif site == "discordbotlist.com":
            embed = self.bot.fn.embed(user, "abc.xyz",
                    f"User voted for FBot!")
        elif site == "botsfordiscord.com":
            salary = self.vote_rewards(user_id)
            embed = self.bot.fn.embed(user, site,
                    f"{name} voted and gained **~~f~~ {salary}**")
        await self.voteschannel(embed=embed)
            

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        user_id = data["user"]
        self.bot.db.register(user_id)
        try: name = await self.bot.fetch_user(user_id).name
        except: name = "User"
            
        embed = self.bot.fn.embed(user, "top test",
                f"{name} tested out the webhook")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user_id = data["user"]
        self.bot.db.register(user_id)
        try: name = await self.bot.fetch_user(user_id).name
        except: name = "User"

        salary = self.vote_rewards(user_id)
        embed = self.bot.fn.embed(user, "top.gg",
                f"{name} voted and gained **~~f~~ {salary}**")
        await self.voteschannel(embed=embed)
    
def setup(bot):
    bot.add_cog(economy(bot))

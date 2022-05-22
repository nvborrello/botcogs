from redbot.core import commands
from discord.ext import tasks

class PokeCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, pokemon: str):
        global spam_loop

        @tasks.loop(seconds=1)
        async def spam_loop(q):
            await ctx.send(q)

        spam_loop.start(pokemon)
        await ctx.send("Now spamming " + pokemon)

    @commands.command()
    async def stopspam(self, ctx):
        spam_loop.cancel()
        await ctx.send("Stopped spamming")
       
    @commands.command()
    async def fuckbrian(self, ctx):
        await ctx.send("User: " + ctx.author +  "Hey Brian, fuck you!")

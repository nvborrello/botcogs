from redbot.core import commands
from discord.ext import tasks

class PokeCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startsearch(self, ctx: commands.Context, pokemon: str):
        global spam_loop

        @tasks.loop(seconds=1)
        async def spam_loop(q):
            await self.bot.say(q)

        spam_loop.start(pokemon)
        await self.bot.say("Now spamming " + str(pokemon))

    @commands.command()
    async def stopsearch(self, ctx: commands.Context):
        spam_loop.cancel()
        await ctx.send("Stopped spamming")

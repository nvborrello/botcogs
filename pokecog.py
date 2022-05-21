from redbot.core import commands
from discord.ext import tasks

class PokeCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startsearch(self, ctx, pokemon: str):
        # global spam_loop

        # @tasks.loop(seconds=1)
        # async def spam_loop(q):
        #     await ctx.send(q)

        # spam_loop.start(pokemon)
        await ctx.send("Now spamming " + pokemon)

    # @commands.command()
    # async def stopsearch(self, ctx: commands.Context):
    #     spam_loop.cancel()
    #     await ctx.send("Stopped spamming")

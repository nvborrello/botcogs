from redbot.core import commands
from discord.ext import tasks

class SpamCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def starttospam(self, ctx, spam: str):
        global spam_loop

        @tasks.loop(seconds=1)
        async def spam_loop(q):
            await ctx.send(q)

        spam_loop.start(spam)
        await ctx.send("Now spamming " + spam)

    @commands.command()
    async def stopthespam(self, ctx):
        spam_loop.cancel()
        await ctx.send("Stopped spamming")
       
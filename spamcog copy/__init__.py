from .spamcog import SpamCog


def setup(bot):
    bot.add_cog(SpamCog(bot))
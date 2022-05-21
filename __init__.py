from .pokecog import PokeCog


def setup(bot):
    bot.add_cog(PokeCog(bot))
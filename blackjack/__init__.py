from .blackjack import BlackJack


def setup(bot):
    bot.add_cog(BlackJack(bot))

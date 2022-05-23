from redbot.core import commands
from discord.ext import tasks
import random

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(1, 14):
                self.cards.append(Card(s, v))

class BlackJack(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        deck = Deck()
        deck.build
        user = ctx.author
        await ctx.send(f'Starting a game of Blackjack...\n {user} has bet ${bet}')

        yourcards = random.sample(deck.cards, 2)
        await ctx.send(f'Your cards are {yourcards[0]} and {yourcards[1]}')
        reply = await self.wait_for("message")

       
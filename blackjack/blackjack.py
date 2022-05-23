from redbot.core import commands
from discord.ext import tasks
import random

deck = []

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
    def toString(self):
        return (f'{self.value} of {self.suit}')

for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
    for v in range(1, 14):
        deck.append(Card(s, v))

class BlackJack(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        user = ctx.author
        await ctx.send(f'Starting a game of Blackjack...\n {user} has bet ${bet}')
        drawn = random.sample(deck, 2)
        str1 = drawn[0].toString()
        str2 = drawn[1].toString()
        await ctx.send(str1)
        await ctx.send(str2)
        await ctx.send(f'Card 1: {drawn[0].value} of {drawn[0].suit}\nCard 2: {drawn[1].value} of {drawn[1].suit}')

       
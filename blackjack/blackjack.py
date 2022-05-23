import math
from redbot.core import commands
from discord.ext import tasks
import random

deck = []

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def print(self):
        curVal = int(self.value)
        newValue = ''
        if curVal > 10:
            match (curVal-10):
                case 1:
                    newValue = 'King'
                case 2:
                    newValue = 'Queen'
                case 3:
                    newValue = 'Ace'
                case 4:
                    newValue = 'Jack'
        else:
            newValue = self.value
        printer = f'{newValue} of {self.suit}'
        return printer

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
        await ctx.send(f'Card 1: {drawn[0].print()}\nCard 2: {drawn[1].print()}')

       
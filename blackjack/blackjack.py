from redbot.core import commands
from discord.ext import tasks
import random

deck = []

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
    for v in range(1, 14):
        stringy = ''
        if v > 10:
            match (v-10):
                case 1:
                    stringy = 'Ace'
                case 2:
                    stringy = 'King'
                case 3:
                    stringy = 'Queen'
                case 4:
                    stringy = 'Jack'
        else:
            stringy = v
        deck.append(Card(s, stringy))


class BlackJack(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        user = ctx.author
        await ctx.send(f'Starting a game of Blackjack...\n {user} has bet ${bet}')
        drawn = random.sample(deck, 2)
        await ctx.send(f'Card 1: {drawn[0].value} of {drawn[0].suit}\n Card 2: {drawn[1].value} of {drawn[1].suit}')

       
from redbot.core import commands
from discord.ext import tasks
import random

deck = []

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def toString(self):
        if int(self.value) > 10:
            newValue = ''
            i = self.value - 10
            match i:
                case 1:
                    newValue = 'King'
                case 2:
                    newValue = 'Queen'
                case 3:
                    newValue = 'Ace'
                case 4:
                    newValue = 'Jack'
            return (f'{newValue} of {self.suit}')
        else:
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
        gameMode = 0
        gameActive = True

        while gameActive:
            match gameMode:
                case 1:

                    player = random.sample(deck, 2)
                    str1 = player[0].toString()
                    str2 = player[1].toString()

                    house = random.sample(deck, 2)
                    str3 = house[0].toString()
                    str4 = house[1].toString()

                    await ctx.send(f'Your Cards:\nCard 1: {str1}\nCard 2: {str2}\n')
                    await ctx.send(f'Dealer\'s Cards:\nCard 1: {str3}\nCard 2: {str4}')



       
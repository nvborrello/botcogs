from redbot.core import commands
from discord.ext import tasks
import random
import time

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
        gameMode = 'Draw'
        gameActive = True
        playerCards = []

        while gameActive:
            match gameMode:
                case 'Draw':
                    player = random.sample(deck, 2)
                    str1 = player[0].toString()
                    str2 = player[1].toString()
                    deck.remove(player[0])
                    deck.remove(player[1])
                    playerCards.append(player[0])
                    playerCards.append(player[1])

                    house = random.sample(deck, 2)
                    str3 = house[0].toString()
                    str4 = house[1].toString()
                    deck.remove(house[0])
                    deck.remove(house[1])

                    await ctx.send(f'Your Cards:\n{playerCards}\n')
                    await ctx.send("\nWould you like to draw another card? (y/n)")
                        
                case 'Continue':
                    player = random.sample(deck, 1)
                    deck.remove(player[0])
                    playerCards.append(player[0])
                    await ctx.send(f'Your Cards:\n{playerCards}\n')






       
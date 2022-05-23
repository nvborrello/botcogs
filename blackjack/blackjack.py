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
            if gameMode == 'Draw':
                player = random.sample(deck, 2)
                deck.remove(player[0])
                deck.remove(player[1])
                playerCards.append(player[0].toString())
                playerCards.append(player[1].toString())

                house = random.sample(deck, 2)
                deck.remove(house[0])
                deck.remove(house[1])

                await ctx.send(f'Your Cards:\n{playerCards}\n')
                time.sleep(1)
                await ctx.send("\nWould you like to draw another card? (y/n)")
                msg = await self.wait_for('message', check=check, timeout=10)

                if msg.content == 'y' or 'Y':
                    gameMode == 'Continue'
                else:
                    gameMode == 'Flip'

            if gameMode == 'Continue':
                player = random.sample(deck, 1)
                deck.remove(player[0])
                playerCards.append(player[0].toString())
                await ctx.send(f'Your Cards:\n{playerCards}\n')
                time.sleep(1)
                await ctx.send("\nWould you like to draw another card? (y/n)")
                msg = await self.wait_for('message', check=check, timeout=10)
                # if msg.content == 'y' or 'Y':
                #     gameMode == 'Continue'
                # else:
                #     gameMode == 'Flip'
            
            if gameMode == 'Flip':
                await ctx.send(f'Your Cards:\n{playerCards}\n')




       
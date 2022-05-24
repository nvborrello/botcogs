from glob import glob
from tkinter.tix import Tree
from redbot.core import commands
from discord.ext import tasks
import random

deck = []
gameMode = 'Draw'
gameActive = True


class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def toString(self):
        return (f'{self.value} of {self.suit}')
    
def getsum(cards):
    sum = 0
    for card in cards:
        sum+= card.value
    return sum

for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
    for v in range(1, 14):
        deck.append(Card(s, v))

class BlackJack(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def exitjack(self, ctx):
        gameMode = "Exit"
        gameActive = False

    @commands.command()
    async def blackjack(self, ctx):
        user = ctx.author
        await ctx.send(f'Starting a game of Blackjack with {user}')
        global gameActive
        global gameMode

        playerCards = []

        while gameActive:
            # Game mode when the game is just starting
            currentMode = gameMode
            if currentMode == 'Draw':
                # Draw 2 cards for the player
                player = random.sample(deck, 2)
                deck.remove(player[0])
                deck.remove(player[1])
                playerCards.append(player[0])
                playerCards.append(player[1])

                house = random.sample(deck, 2)
                deck.remove(house[0])
                deck.remove(house[1])

                # Create a list for the cards as strings
                stringList = []
                for card in playerCards:
                    stringList.append(f'{card.value} of {card.suit}')


                # Send user their cards
                await ctx.send(f'Your Cards:\n{stringList}\nTotal Value: {getsum(playerCards)}')
                await ctx.send("\nWould you like to draw another card? (y/n)")

                # Response Checker
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                msg = await self.bot.wait_for('message', check=check)
                
                if msg.content.lower in ("y", "yes"):
                    gameMode == 'Continue'
                    await ctx.send(f"\nGamemode = {gameMode}")
                else:
                    gameMode == 'Flip'
                    await ctx.send(f"\nGamemode = {gameMode}")


            # Game mode if the player decides to draw another card
            if currentMode == 'Continue':
                # Draw another card
                player = random.sample(deck, 1)
                deck.remove(player[0])
                playerCards.append(player[0].toString())

                # Send player their cards
                await ctx.send(f'Your Cards:\n{playerCards}\nTotal Value: {getsum(playerCards)}')
                await ctx.send("\nWould you like to draw another card? (y/n)")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                msg = await self.bot.wait_for('message', check=check)

                if msg.content.lower in ("y", "yes"):
                    gameMode == 'Continue'
                    await ctx.send(f"\nGamemode = {gameMode}")
                else:
                    gameMode == 'Flip'
                    await ctx.send(f"\nGamemode = {gameMode}")
            
            if currentMode == 'Flip':
                await ctx.send(f"\nGamemode = {gameMode}")
                await ctx.send(f'Your Final Cards:\n{playerCards}\n')
                break

            if currentMode == 'Exit':
                await ctx.send(f"\nGamemode = {gameMode}")
                await ctx.send('Exiting Game')
                break




       
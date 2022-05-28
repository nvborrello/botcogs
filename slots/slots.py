import asyncio
from tkinter import NW
from redbot.core import commands
from discord.ext import tasks
import random
import time
import economy as economy

# init the globals and other stuff
economy.init()
ITEMS = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR"]


# Create a wheel with different symbols
class Wheels:
    def __init__(self, sym, n: int):
        self.symbols = sym
        self.n = n

    def spin(self):
        spins = []
        for x in range(self.n):
            spins.append(random.choice(self.symbols, 1))
        return spins

# Create the wheels for the machine
machine = Wheels(ITEMS, 3)

# Grabs the user's money balance
def getMoney(userID):
    if userID in economy.money:
        return economy.money[userID]
    else:
        economy.money.update({userID: 1000})
        return 1000

class Slots(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        userid = str(ctx.author.id)
        wins = economy.winloss[userid]['Wins']
        losses = economy.winloss[userid]['Losses']
        await ctx.send(f'You have {wins} wins and {losses} losses.')
    
    @commands.command()
    async def money(self, ctx):
        userid = str(ctx.author.id)
        money = getMoney(userid)
        await ctx.send(f'You have ${money}.')

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        user = ctx.author.mention
        userid = str(ctx.author.id)
        playerMoney = getMoney(userid)        

        if bet > playerMoney:
            await ctx.send(f'*You can\'t bet more then your current balance (${playerMoney})!*')
            return
        
        gameMode = 0
        rounds = 0

        global gameActive
        gameActive = True

        while gameActive:
            
            # Game mode when the game is just starting
            if gameMode == 0:

                await ctx.send(f'*{user} has bet ${bet}! Starting game...*')
                time.sleep(3)

                # Take out bet money
                economy.money[userid]-=bet

                # Spin the wheels
                spins = machine.spin()
                await ctx.send(f'*You spun {spins}*')

                # Show user the wheels
                await ctx.send(f'***Spin test***')
                moreoma = ctx.author.id
                message = await ctx.send("**Do you want to spin again?**")

                emojis = ['✅', '❌']

                # Adds reaction to above message
                for emoji in (emojis):
                    await message.add_reaction(emoji)

                def check(reaction, user):
                    reacted = reaction.emoji
                    return user.id == moreoma and str(reaction.emoji) in emojis

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("*timed out*")
                    break
                else:
                    if reaction.emoji == '✅':
                        gameMode = 0
                    elif reaction.emoji == '❌':
                        gameMode = 1
                        
            # Game mode if the player decides to not spin again
            if gameMode == 1:
                # Exits the spin loop
                return
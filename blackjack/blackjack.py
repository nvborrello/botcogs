import asyncio
from redbot.core import commands
from discord.ext import tasks
import random
import time
import blackjack.economy
deck = []

# Create a card with the suit, num/rank, and the point value
class Card:
    def __init__(self, suit: str, val, pts):
        self.suit = suit
        self.value = val
        self.points = pts

    def toString(self):
        return (f'{self.value} of {self.suit}')

def getsum(cards):
    sum = 0
    hasAce = False
    for card in cards:
        sum+= card.points
        if card.value == 'Ace':
            hasAce = True
    if hasAce and sum <= 11:
        sum+=10
    return sum

# Grabs the user's money balance
def getMoney(userID):
    if userID in blackjack.economy.money:
        return blackjack.economy.money[userID]
    else:
        blackjack.economy.money.update({userID: 1000})
        return 1000

def updateWL(userID, winBool, bet):
    if winBool:
        if userID in blackjack.economy.winloss:
            blackjack.economy.winloss[userID]['Wins']+=1
            blackjack.economy.money[userID]+=(bet*2)
        else:
            blackjack.economy.winloss.update({userID: {'Wins': 1, 'Losses': 0}})
            blackjack.economy.money[userID]+=(bet*2)
    elif not winBool:
        if userID in blackjack.economy.winloss:
            blackjack.economy.winloss[userID]['Losses']+=1
            blackjack.economy.money[userID]-=bet
        else:
            blackjack.economy.winloss.update({userID: {'Wins': 0, 'Losses': 1}})
            blackjack.economy.money[userID]-=bet

for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
    for v in range(1, 14):
        if v == 1:
            deck.append(Card(s, 'Ace', 1))
        elif v == 11:
            deck.append(Card(s, 'King', 10))
        elif v == 12:
            deck.append(Card(s, 'Queen', 10))
        elif v == 13:
            deck.append(Card(s, 'Jack', 10))
        else:
            deck.append(Card(s, v, v))

class BlackJack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        userid = str(ctx.author.id)
        wins = blackjack.economy.winloss[userid]['Wins']
        losses = blackjack.economy.winloss[userid]['Losses']
        await ctx.send(f'You have {wins} wins and {losses} losses.')

    @commands.command()
    async def exitjack(self, ctx):
        global gameActive
        gameActive = False
        await ctx.send('Stopped')

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        user = ctx.author.mention
        userid = str(ctx.author.id)
        playerMoney = getMoney(userid)

        if bet > playerMoney:
            await ctx.send(f'*You can\'t bet more then your current balance (${playerMoney})!*')
            return

        await ctx.send(f'*{user} has bet ${bet}! Starting game...*')
        time.sleep(3)
        
        gameMode = 0
        rounds = 0

        global gameActive
        gameActive = True


        playerCards = []
        botCards = []
        stringList = []
        botList = []

        while gameActive:
            
            # Game mode when the game is just starting
            if gameMode == 0:

                # Draw player's cards
                player = random.sample(deck, 2)
                deck.remove(player[0])
                deck.remove(player[1])
                playerCards.append(player[0])
                playerCards.append(player[1])

                # Draw house's cards
                house = random.sample(deck, 2)
                deck.remove(house[0])
                deck.remove(house[1])
                botCards.append(house[0])
                botCards.append(house[1])

                # Create a list for user's cards as strings
                stringList = []
                for card in playerCards:
                    stringList.append(card.toString())
                # Create a list for bot's cards as strings
                botList = []
                for card in botCards:
                    botList.append(card.toString())

                hideList = [botList[0], '?']
                currentSum = getsum(playerCards)

                # Send user their cards
                playerClean = ', '.join(stringList)
                botClean = ', '.join(hideList)
                await ctx.send(f'***You drew a {player[0].toString()} and a {player[1].toString()}***')
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**Bot\'s Cards:**\n{botClean}\nTotal Value: ?')
                moreoma = ctx.author.id
                message = await ctx.send("**Do you want to draw another card?**")

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
                        gameMode = 1
                    elif reaction.emoji == '❌':
                        gameMode = 2
                        
            # Game mode if the player decides to draw another card
            if gameMode == 1:
                # Draw another card

                player = random.sample(deck, 1)
                deck.remove(player[0])
                playerCards.append(player[0])

                # Create a list for the cards as strings
                stringList = []
                for card in playerCards:
                    stringList.append(card.toString())

                currentSum = getsum(playerCards)

                # Send player their cards
                playerClean = ', '.join(stringList)
                await ctx.send(f'***You drew a {player[0].toString()}***')
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**Bot\'s Cards:**\n{botClean}\nTotal Value: ?')

                if currentSum > 21:
                    gameMode = 3
                    continue

                moreoma = ctx.author.id
                message = await ctx.send("**Do you want to draw another card?**")

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
                        gameMode = 1
                    elif reaction.emoji == '❌':
                        gameMode = 2
            
            # Game mode when the player no longer wants to draw another card
            if gameMode == 2:

                # Create a list for the bot's cards as strings
                stringList = []
                for card in playerCards:
                    stringList.append(card.toString())

                botScore = getsum(botCards)

                # Send results
                playerClean = ', '.join(stringList)
                botClean = ', '.join(botList)
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**Bot\'s Cards:**\n{botClean}\nTotal Value: {getsum(botCards)}')

                time.sleep(2)

                # Have dealer draw if under 17
                if botScore < 17:
                    while True:
                        # have the bot draw a card
                        await ctx.send(f'*Bot\'s sum is below 17, drawing again...*')
                        time.sleep(2)
                        bot = random.sample(deck, 1)
                        deck.remove(bot[0])
                        botCards.append(bot[0])
                        await ctx.send(f'*Bot drew a {bot[0].toString()}*\nTotal Value: {getsum(botCards)}')

                        # Recalculate the bots score
                        botScore = getsum(botCards)
                        if botScore > 21 or botScore > 16:
                            break
                
                time.sleep(2)

                if botScore > 21:
                    gameMode = 4
                    continue

                # Determine Winner
                playerFinal = getsum(playerCards) 
                botFinal = getsum(botCards)
                if botFinal > playerFinal:
                    await ctx.send('**Bot Wins!**')
                    updateWL(userid, False, bet)
                elif botFinal < playerFinal:
                    await ctx.send('**You win!**')
                    updateWL(userid, True, bet)
                elif botFinal == playerFinal:
                    await ctx.send('**It\'s a Tie!**')
                break

            # Player went over 21
            if gameMode == 3:
                await ctx.send('**You went over 21! Bot wins!**')
                updateWL(userid, False, bet)
                break

            # Bot went over 21
            if gameMode == 4:
                await ctx.send('**Bot went over 21! You win!**')
                updateWL(userid, True, bet)
                break




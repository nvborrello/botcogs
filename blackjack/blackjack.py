from redbot.core import commands
from discord.ext import tasks
import random
import time

deck = []


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
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def exitjack(self, ctx):
        global gameActive
        gameActive = False
        await ctx.send('Stopped')

    @commands.command()
    async def blackjack(self, ctx):
        user = ctx.author.mention
        await ctx.send(f'*Starting a game of Blackjack with {user}*')
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
                await ctx.send(f'*You drew a {player[0].toString()} and a {player[1].toString()}*')
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**Bruno\'s Cards:**\n{botClean}\nTotal Value: ?')
                await ctx.send("\nWould you like to draw another card? (y/n)")

                # Response Checker
                def check(reaction, user):
                    reacted = reaction.emoji
                    return user.id == moreoma and str(reaction.emoji) in emojis

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("timeout")
                else:
                    if str(reacted) == '<:nonatick:803586318369292289>':
                        gameMode = 1
                    elif reaction.emoji == '<:RedTick:801684348502933525>':
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
                await ctx.send(f'*You drew a {player[0].toString()}*')
                await ctx.send(f'**Your Cards**:\n{playerClean}\nTotal Value: {getsum(playerCards)}')

                if currentSum > 21:
                    gameMode = 3
                    continue

                await ctx.send("\nWould you like to draw another card? (y/n)")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                msg = await self.bot.wait_for('message', check=check)

                if msg.content in ("y", "yes"):
                    # Stay in mode 1
                    gameMode = 1
                if msg.content in ("n", "no"):
                    # Flip the cards
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
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**Bruno\'s Cards:**\n{botClean}\nTotal Value: {getsum(botCards)}')

                time.sleep(2)

                # Have dealer draw if under 17
                if botScore < 17:
                    while True:
                        # have the bot draw a card
                        await ctx.send(f'*Bruno\'s sum is below 17, drawing again...*')
                        time.sleep(2)
                        bot = random.sample(deck, 1)
                        deck.remove(bot[0])
                        botCards.append(bot[0])
                        await ctx.send(f'*Bruno drew a {bot[0].toString()}*\nTotal Value: {getsum(botCards)}')

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
                    await ctx.send('**Bruno Wins!**')
                elif botFinal < playerFinal:
                    await ctx.send('**You win!**')
                elif botFinal == playerFinal:
                    await ctx.send('**It\'s a Tie!**')
                break

            # Player went over 21
            if gameMode == 3:
                await ctx.send('**You went over 21! Bruno wins!**')
                break

            # Bot went over 21
            if gameMode == 4:
                await ctx.send('**Bruno went over 21! You win!**')
                break





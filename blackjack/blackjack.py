from redbot.core import commands
from discord.ext import tasks
import random

deck = []


class Card:
    def __init__(self, suit: str, val):
        self.suit = suit
        self.value = val

    def toString(self):
        return (f'{self.value} of {self.suit}')

def getsum(cards):
    sum = 0
    for card in cards:
        if isinstance(card.value, str):
            if card.value == 'Ace':
                sum+=11
            else:
                sum+=10
        else:
            sum+= card.value
    return sum

for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
    for v in range(1, 14):
        if v == 1:
            deck.append(Card(s, 'Ace'))
        elif v == 11:
            deck.append(Card(s, 'King'))
        elif v == 12:
            deck.append(Card(s, 'Queen'))
        elif v == 13:
            deck.append(Card(s, 'Jack'))
        else:
            deck.append(Card(s, v))

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
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**My Cards:**\n{botClean}\nTotal Value: ?')
                await ctx.send("\nWould you like to draw another card? (y/n)")

                # Response Checker
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                msg = await self.bot.wait_for('message', check=check)
                
                if msg.content in ("y", "yes"):
                    gameMode = 1
                if msg.content in ("n", "no"):
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
                await ctx.send(f'You drew a {player[0].toString()}')
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
                await ctx.send(f'**Your Cards:**\n{playerClean}\nTotal Value: {getsum(playerCards)}\n\n**My Cards:**\n{botClean}\nTotal Value: {getsum(botCards)}')
                if botScore > 21:
                    gameMode = 4
                    continue

                # Have dealer draw if under 17
                if botScore < 17:
                    while True:
                        # have the bot draw a card
                        await ctx.send(f'My sum below 17, drawing again...')
                        bot = random.sample(deck, 1)
                        deck.remove(bot[0])
                        botCards.append(bot[0])
                        await ctx.send(f'I drew a {bot[0].toString()}\nTotal Value: {getsum(botCards)}')

                        # Recalculate the bots score
                        botScore = getsum(botCards)
                        if botScore > 21:
                            gameMode = 4
                            break
                        elif botScore > 16:
                            break


                # Determine Winner
                playerFinal = getsum(playerCards) 
                botFinal = getsum(botCards)
                if botFinal > playerFinal:
                    await ctx.send('You Lost :PogOFF:')
                else:
                    await ctx.send('You win!')
                break

            # Player went over 21
            if gameMode == 3:
                await ctx.send('You went over 21! You lose!')
                break

            # Bot went over 21
            if gameMode == 4:
                await ctx.send('Bot went over 21! You win!')
                break





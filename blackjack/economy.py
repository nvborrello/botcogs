# Global variable for all players wins, losses, and money

from glob import glob


def init():
    global winloss
    winloss = {}
    global money
    money = {}

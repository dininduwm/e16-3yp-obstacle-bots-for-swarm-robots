import random
import math
from robot import robot

# set to hold the working robots
workingBots = set()

# all the bots
allBots = set()

# message bots
messageBots = set()

# maping the bots with destination to the bot index
botMapping = {}

# function to create the string format
def createString(data):
    return str(data['x']) + '-' + str(data['y'])

# function to create string from; bots
def createStringBots(_robot):
    return str(_robot.des_pos[0]) + '-' + str(_robot.des_pos[1])

# function to create touple using the hash string
def createTuple(string):
    tmp = string.split('-')
    return ((int(tmp[0]), int(tmp[1])))

# function to calculate the distance
def calcDistance(str1, str2):
    t1 = createTuple(str1)
    t2 = createTuple(str2)
    x1 = t1[0]
    x2 = t2[0]
    y1 = t1[1]
    y2 = t2[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# function to find the least distance bot
def leastDistBot(idleBots, dest):
    minDist = float('inf')
    minBot = ''
    for _bot in idleBots:
        distance = calcDistance(_bot, dest)
        if distance < minDist:
            minDist = distance
            minBot = _bot
    return minBot

# function to assign a bot
def assignBot(listOfDest, robotList):
    global allBots, workingBots, botMapping, messageBots
    # find the idle bots
    idleBots = allBots - workingBots

    for dest in listOfDest:
        if (len(idleBots) == 0):
            print('No free bots')
        else:
            selectedBot = leastDistBot(idleBots, dest)
            selBot = robotList[botMapping[selectedBot]]
            selBot.des_pos = createTuple(dest)
            selBot.idle = False
            idleBots.remove(selectedBot)
            workingBots.add(dest)


# function to idle the bots
def idleBot(listOfBots, robotList):
    global allBots, workingBots, botMapping, messageBots

    for bot in listOfBots:
        workingBots.remove(bot)
        robotList[botMapping[bot]].idle = True

# def new message
def arrageBot(robotList, message):
    global allBots, workingBots, botMapping, messageBots
    allBots = set()
    messageBots = set()
    botMapping = {}

    # loop through the robot list and add to the all robot list
    for index in range(len(robotList)):
        _robot = robotList[index]
        allBots.add(createStringBots(_robot))
        botMapping[createStringBots(_robot)] = index

    # loop through the list and find the messege bots
    for des in message:
        messageBots.add(createString(des))

    # find the bots should be idled
    shouldIdle = workingBots - messageBots

    # should assign
    shouldAssign = messageBots - workingBots

    print(allBots)
    print(shouldIdle)
    print(shouldAssign)
    print('\n')

    # idling the bots
    idleBot(shouldIdle, robotList)

    # assigning the bots
    assignBot(shouldAssign, robotList)


# BOT_COUNT = 8
# ARENA_DIM = 30
# robots_data = []


# def initialize():
#     global robots_data
#     for i in range(BOT_COUNT):
#         robots_data.append(
#             robot(
#                 # TODO the corner bug should be resolved at the client
#                 (random.randint(5, ARENA_DIM-5), random.randint(5, ARENA_DIM-5)),
#                 0,
#                 (random.randint(5, ARENA_DIM-5), random.randint(5, ARENA_DIM-5)),
#                 0
#             )
#         )

# initialize()
# print(len(robots_data))

# arr = [{'x': 24, 'y': 18}, {'x': 24, 'y': 12}, {'x': 21, 'y': 11},
#        {'x': 27, 'y': 16}, {'x': 22, 'y': 27}, {'x': 28, 'y': 23}]

# arrageBot(robots_data, arr)

# arr = [{'x': 24, 'y': 18}, {'x': 24, 'y': 12}, {'x': 21, 'y': 11},
#        {'x': 27, 'y': 16}, {'x': 22, 'y': 27}, {'x': 28, 'y': 24}]

# arrageBot(robots_data, arr)
# arrageBot(robots_data, arr)

import os
import Levels

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 840
CART_WIDTH = 140
CART_HEIGHT = 100
CART_WEIGHT = 1
INVADER_WIDTH = 70
INVADER_HEIGHT = 70
BULLET_ANGLE = 60
BULLET_RADIUS = 30
interval_for_cart = 1000
interval_for_score = 1000
CAN_MOVE_DOWN = False
AIM_CART = 'AIM_CART'
BAD_AIM_CART = 'BAD_AIM_CART'
AIM_RANDOM = 'AIM_RANDOM'
RIGHT = "RIGHT"
LEFT = "LEFT"
NOPE = "NOPE"
cwd = os.getcwd()
hard_invader_lives = 3
medium_invader_lives = 2
easy_invader_lives = 1
lives = [easy_invader_lives, medium_invader_lives, hard_invader_lives]
easyInvadersCount = 0
mediumInvadersCount = 0
hardInvadersCount = 0
interval_for_invaders = 0
current_type = ''
bunkersCount = 0

levels = Levels.levels(1)
txt = levels.parse_level()
easyInvadersCount = int(txt[0])
mediumInvadersCount = int(txt[1])
hardInvadersCount = int(txt[2])
interval_for_invaders = int(txt[3])
if txt[4] == 1:
    current_type = AIM_CART
if txt[4] == 2:
    current_type = BAD_AIM_CART
else:
    current_type = AIM_RANDOM
bunkersCount = int(txt[5])

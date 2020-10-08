from PyQt5.QtGui import QImage
import os


def our_QImage(file):
    return QImage(os.path.join('pictures', file))


BACKGROUND = our_QImage('background.png')
CARTLU = our_QImage('cartLU.png')
CARTLD = our_QImage('cartLD.png')
CARTRU = our_QImage('cartRU.png')
CARTRD = our_QImage('cartRD.png')
INVADER = our_QImage('invader.png')
MEDIUM_INVADER = our_QImage('invader2.png')
HARD_INVADER = our_QImage('invader3.png')
BULLET1 = our_QImage('bullet1.png')
BULLET2 = our_QImage('bullet2.png')
BULLET3 = our_QImage('bullet3.png')
BULLET = [BULLET1, BULLET2, BULLET3]
OUR_BULLET = our_QImage('our_bullet.png')
BUNKER_1 = our_QImage('bunker1.png')
BUNKER_2 = our_QImage('bunker2.png')
BUNKER_3 = our_QImage('bunker3.png')
live_line = our_QImage('life_line')
line_full = our_QImage('line_full')
GAME_OVER = our_QImage('game_over.png')
PAUSE = our_QImage('pause.png')
ZERO = our_QImage('0.png')
ONE = our_QImage('1.png')
TWO = our_QImage('2.png')
THREE = our_QImage('3.png')
FOUR = our_QImage('4.png')
FIVE = our_QImage('5.png')
SIX = our_QImage('6.png')
SEVEN = our_QImage('7.png')
EIGHT = our_QImage('8.png')
NINE = our_QImage('9.png')
BULLET_BONUS = our_QImage('bullet_bonus.png')
HEALTH = our_QImage('health.png')
MYSTERY_SHIP = our_QImage('mystery_ship.png')
SCOREBOARD = our_QImage('scoreboard.png')
SAVE = our_QImage('SAVE.png')
BUNKERS = [BUNKER_3, BUNKER_2, BUNKER_1]
INVADERS = [INVADER, MEDIUM_INVADER, HARD_INVADER]
ARR = [ZERO, ONE, TWO, THREE, FOUR, FIVE,
       SIX, SEVEN, EIGHT, NINE]

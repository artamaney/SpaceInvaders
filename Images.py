from PyQt5.QtGui import QImage
import Values


def our_QImage(file):
    return QImage(f'{Values.cwd}\\pictures\\{file}')


BACKGROUND = our_QImage('background.png')
CARTLU = our_QImage('cartLU.png')
CARTLD = our_QImage('cartLD.png')
CARTRU = our_QImage('cartRU.png')
CARTRD = our_QImage('cartRD.png')
INVADER = our_QImage('invader.png')
MEDIUM_INVADER = our_QImage('invader2.png')
HARD_INVADER = our_QImage('invader3.png')
BULLET = our_QImage('bullet.png')
BUNKER_1 = our_QImage('bunker1.png')
BUNKER_2 = our_QImage('bunker2.png')
BUNKER_3 = our_QImage('bunker3.png')
GAME_OVER = our_QImage('game_over.png')
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
ARR = [ZERO, ONE, TWO, THREE, FOUR, FIVE,
       SIX, SEVEN, EIGHT, NINE]

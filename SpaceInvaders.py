from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sys
import Enemies
from random import randint
import Values
import Images


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.pause_mode = False
        self.count = 0
        self.game_is_over = False
        self.flag = True
        self.title = "SPACE INVADERS"
        self.BACKGROUND = Images.BACKGROUND
        self.ICON = QIcon('space-invader-icon.png')
        self.width = Values.WINDOW_WIDTH
        self.height = Values.WINDOW_HEIGHT
        self.invaders = self.init_invaders()
        self.bullets = []
        self.bullets_inv = []
        self.cart = Enemies.Cart(50, 530, Values.CART_WIDTH,
                                 Values.CART_HEIGHT, Values.CART_WEIGHT, 3)
        self.bunkers = self.init_bunkers()
        self.score = Enemies.Score(0)
        self.timer_update = QtCore.QTimer()
        self.timer_update.timeout.connect(self.update)
        self.timer_update.start(5)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.cart_fire())
        self.timer.timeout.connect(lambda: self.move_invaders())
        self.timer.timeout.connect(lambda: self.invader_fire())
        self.timer.timeout.connect(lambda: self.cart.
                                   intersect_cart(self.bullets_inv))
        self.timer.timeout.connect(lambda: self.score.
                                   intersect_cart(self.bullets_inv, self.cart))
        self.timer.timeout.connect(lambda: self.score.
                                   intersect_invader(self.bullets,
                                                     self.invaders))
        self.timer.timeout.connect(lambda: self.intersection_bullet_invader())
        self.timer.timeout.connect(lambda: self.kill_bunker())
        self.timer.timeout.connect(lambda: self.cart.move(
            Values.NOPE, int(not self.pause_mode) / 2))
        self.timer.start(5)
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(lambda: self.invader_makes_bullets())
        self.timer2.start(Values.interval_for_invaders)
        self.timer3 = QtCore.QTimer()
        self.timer3.timeout.connect(lambda: self.score.reduce())
        self.timer3.start(Values.interval_for_score)
        self.able_fire = False
        self.timer4 = QtCore.QTimer()
        self.timer4.timeout.connect(lambda: self.able_to_fire())
        self.timer4.start(Values.interval_for_cart)
        self.initUI()

    def initUI(self):
        self.initBackground(self.BACKGROUND)
        self.setWindowIcon(self.ICON)
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.show()

    def paintEvent(self, paintEvent):
        painter = QtGui.QPainter(self)
        self.print_cart(painter)
        for bunker in self.bunkers:
            self.print_bunker(painter, bunker)
        for bullet in self.bullets:
            self.print_our_bullet(painter, bullet)
        for invader in self.invaders:
            self.print_invaders(painter, invader)
        for bullet in self.bullets_inv:
            self.print_invader_bullet(painter, bullet)
        for invader in self.invaders:
            self.print_lives(painter, invader)
        self.print_cart_lives(painter, self.cart)
        if self.cart.lives <= 0:
            self.game_is_over = True
            self.print_game_over(painter)
        self.print_score(painter)
        self.print_pause(painter)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_P:
            self.pause_mode = not self.pause_mode
            if self.pause_mode:
                self.timer.stop()
                self.timer2.stop()
                self.timer3.stop()
                self.timer4.stop()
            else:
                self.timer.start()
                self.timer2.start()
                self.timer3.start()
                self.timer4.start()

        if not (self.pause_mode or self.game_is_over):
            if key == QtCore.Qt.Key_Right:
                self.cart.move(Values.RIGHT, 4)
                self.cart.direction = Values.RIGHT
            if key == QtCore.Qt.Key_Left:
                self.cart.move(Values.LEFT, 4)
            self.cart.direction = Values.LEFT
            if key == QtCore.Qt.Key_Space and self.able_fire:
                bullet = Enemies.Cart_Bullet(self.cart.x_left,
                                             self.cart.y_top + 2,
                                             Values.BULLET_RADIUS,
                                             Values.BULLET_RADIUS,
                                             Values.BULLET_ANGLE)
                self.bullets.append(bullet)
                self.timer4.start(Values.interval_for_cart)
                self.able_fire = False

    def able_to_fire(self):
        self.able_fire = True

    def print_score(self, painter):
        score = self.find_score()
        for i in range(5):
            rect_score = QtCore.QRect(1000 - 50 * i, 20, 50, 50)
            painter.drawImage(rect_score, Images.ARR[int(score[i])])

    def print_cart(self, painter):
        rect_cart = QtCore.QRect(self.cart.x_left, self.cart.y_top,
                                 self.cart.width, self.cart.height)
        if self.cart.x_left < Values.WINDOW_WIDTH / 2 - 30:
            img = Images.CARTRD
            if self.cart.direction == Values.LEFT:
                img = Images.CARTLU
        else:
            img = Images.CARTLD
            if self.cart.direction == Values.RIGHT:
                img = Images.CARTRU
        painter.drawImage(rect_cart, img)

    def print_pause(self, painter):
        if self.pause_mode:
            rect_pause = QtCore.QRect(Values.WINDOW_WIDTH // 2 - 200,
                                      Values.WINDOW_HEIGHT // 2 - 200, 400, 200)
            painter.drawImage(rect_pause, Images.PAUSE)

    @staticmethod
    def print_lives(painter, invader):
        rect_lives = QtCore.QRect(invader.x_left + 5,
                                  invader.y_top + invader.height,
                                  60, 5)
        full_value = Values.lives[invader.level - 1]
        rect_our_lives = QtCore.QRect(invader.x_left + 5,
                                      invader.y_top + invader.height,
                                      int(invader.lives * 60 / full_value),
                                      5)
        painter.drawImage(rect_lives, Images.live_line)
        painter.drawImage(rect_our_lives, Images.line_full)

    @staticmethod
    def print_cart_lives(painter, cart):
        rect_lives = QtCore.QRect(900, 750, 160, 60)
        rect_our_lives = QtCore.QRect(900, 750, int(cart.lives * 160 / 3), 60)
        painter.drawImage(rect_lives, Images.live_line)
        painter.drawImage(rect_our_lives, Images.line_full)

    @staticmethod
    def print_bunker(painter, bunker):
        rect_bunker = QtCore.QRect(bunker.x_left, bunker.y_top,
                                   bunker.width, bunker.height)
        if bunker.lives == 3:
            image_bunker = Images.BUNKER_1
        elif bunker.lives == 2:
            image_bunker = Images.BUNKER_2
        else:
            image_bunker = Images.BUNKER_3
        painter.drawImage(rect_bunker, image_bunker)

    @staticmethod
    def print_invaders(painter, invader):
        rect_invader = QtCore.QRect(invader.x_left, invader.y_top,
                                    invader.width, invader.height)
        img = Images.INVADER
        if invader.level == 3:
            img = Images.HARD_INVADER
        elif invader.level == 2:
            img = Images.MEDIUM_INVADER
        painter.drawImage(rect_invader, img)

    @staticmethod
    def print_our_bullet(painter, bullet):
        rect_bullet = QtCore.QRect(bullet.x_left, bullet.y_top,
                                   Values.BULLET_RADIUS, Values.BULLET_RADIUS)
        painter.drawImage(rect_bullet, Images.OUR_BULLET)

    @staticmethod
    def print_invader_bullet(painter, bullet):
        rect_bullet = QtCore.QRect(bullet.x_left, bullet.y_top,
                                   Values.BULLET_RADIUS, Values.BULLET_RADIUS)
        level = bullet.invader.level
        img = Images.BULLET[level - 1]
        painter.drawImage(rect_bullet, img)

    @staticmethod
    def print_game_over(painter):
        rect_game_over = QtCore.QRect(240, 140, 500, 380)
        painter.drawImage(rect_game_over, Images.GAME_OVER)

    def initBackground(self, background):
        scaled_bckgrnd = background.scaled(QSize(self.width, self.height))
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(scaled_bckgrnd))
        self.setPalette(palette)

    def cart_fire(self):
        if not self.pause_mode:
            for bullet in self.bullets:
                bullet.move(3)
                if bullet.y_top + bullet.height >= 850:
                    self.bullets.remove(bullet)

    def invader_makes_bullets(self):
        if not self.game_is_over and len(self.invaders) > 0 and not \
                self.pause_mode:
            invader = self.invaders[randint(0, len(self.invaders) - 1)]
            bullet = Enemies.Invader_Bullet(invader.x_left, invader.y_top,
                                            Values.BULLET_RADIUS,
                                            Values.BULLET_RADIUS,
                                            self.cart, 1, invader.lives,
                                            Values.current_type, invader)
            self.bullets_inv.append(bullet)

    def invader_fire(self):
        if not (self.game_is_over or self.pause_mode):
            for bullet in self.bullets_inv:
                bullet.move()
                if bullet.y_top + bullet.height >= 800:
                    self.bullets_inv.remove(bullet)

    def get_left_invader_x(self):
        return sorted(self.invaders,
                      key=lambda invad: invad.x_left)[0].x_left

    def get_right_invader_x(self):
        return sorted(self.invaders,
                      key=lambda invad: invad.x_left, reverse=True)[0].x_left

    def move_invaders(self):
        if not (self.game_is_over or self.pause_mode):
            step = 0.1
            for invader in self.invaders:
                if Values.CAN_MOVE_DOWN \
                        and self.invaders[len(self.invaders) - 1].y_top < 350:
                    invader.move_down(step * 10)
                    self.count += 1
                    if self.count % len(self.invaders) == 0:
                        Values.CAN_MOVE_DOWN = False
                        self.count = 0
                else:
                    if self.flag:
                        invader.move_right(step)
                        self.flag = self.get_right_invader_x() <= 1000
                        Values.CAN_MOVE_DOWN = not self.flag
                    else:
                        invader.move_left(step)
                        self.flag = self.get_left_invader_x() <= 10
                        Values.CAN_MOVE_DOWN = self.flag

    def intersection_bullet_invader(self):
        for invader in self.invaders:
            invader.intersect_bullet(self.bullets, self.invaders)

    def game_over(self):
        return self.cart.lives <= 0

    def kill_bunker(self):
        for bunker in self.bunkers:
            bunker.bullet_intersection(self.bullets_inv, self.bunkers)

    def find_score(self):
        array = []
        for i in range(0, 5):
            array.append(self.score.score // 10 ** i % 10)
        return array

    @staticmethod
    def init_invaders():
        invaders = []
        count = Values.easyInvadersCount + Values.hardInvadersCount \
                                         + Values.mediumInvadersCount
        medium = Values.mediumInvadersCount
        hard = Values.hardInvadersCount
        hard_v = 3 if hard > 0 else -1
        mid_v = 2 if medium > 0 else -1
        easy_v = 1 if count - hard - medium > 0 else -1
        for i in range(count):
            invaders.append(Enemies.Invader(30 + (i % 6) * 150,
                                            50 + (i // 6 % (count // 3)) * 80,
                                            Values.INVADER_WIDTH,
                                            Values.INVADER_HEIGHT,
                                            max(hard_v, mid_v, easy_v),
                                            max(hard_v, mid_v, easy_v)))
            hard -= 1
            if hard <= 0:
                hard_v = -1
                medium -= 1
            if medium <= 0:
                mid_v = -1
        return invaders

    @staticmethod
    def init_bunkers():
        bunkers = []
        for i in range(Values.bunkersCount):
            bunkers.append(Enemies.Bunker((100 + (i + 1) * 350) % 900,
                                          430, 100, 100, 3))
        return bunkers


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SPACE INVADERS")
    window = MainWindow()
    sys.exit(app.exec_())

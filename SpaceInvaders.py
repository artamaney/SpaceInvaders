from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sys
import Enemies
from random import randint
import Values
import Images
import Levels
import argparse
import copy


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('level', nargs='+')
    return parser


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.levels = createParser().parse_args(sys.argv[1:]).level
        self.level_number = 0
        self.level = Levels.levels(self.levels[self.level_number])
        self.pause_mode = False
        self.scoreboard_mode = False
        self.count = 0
        self.addition_power = 0
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
        self.cart = Enemies.Cart(470, 530, Values.CART_WIDTH,
                                 Values.CART_HEIGHT, self.level.weight_cart,
                                 self.level.lives_cart)
        self.bunkers = self.init_bunkers()
        self.mystery_ship = Enemies.MysteryShip(0, 0, 0, 0,
                                                self.bullets, False)
        self.health_bonus = Enemies.HealthBonus(0, 0, 0, 0, self.cart, 0,
                                                False)
        self.bullet_bonus = Enemies.BulletBonus(0, 0, 0, 0, self.cart, 0,
                                                False)
        self.score = Enemies.Score(0, self.level.mystery_ship_score,
                                   self.level.fire_score)
        self.saving = Enemies.Saving()
        self.saving_count = 0
        self.loading_count = 0
        self.timer_update = QtCore.QTimer()
        self.timer_update.timeout.connect(self.update)
        self.timer_update.start(5)
        self.main_timer = QtCore.QTimer()
        self.main_timer.timeout.connect(lambda: self.cart_fire())
        self.main_timer.timeout.connect(lambda: self.move_invaders())
        self.main_timer.timeout.connect(lambda: self.invader_fire())
        self.main_timer.timeout.connect(lambda: self.score.intersect_cart
                                        (self.bullets_inv, self.cart))
        self.main_timer.timeout.connect(lambda: self.cart.intersect_cart
                                        (self.bullets_inv))
        self.main_timer.timeout.connect(lambda: self.init_bonuses())
        self.main_timer.timeout.connect(lambda: self.score.intersect_invader
                                        (self.bullets, self.invaders))
        self.main_timer.timeout.connect(lambda:
                                        self.intersection_bullet_invader())
        self.main_timer.timeout.connect(lambda: self.kill_bunker())
        self.main_timer.timeout.connect(lambda: self.cart.move(Values.NOPE))
        self.main_timer.timeout.connect(lambda: self.win())
        self.main_timer.timeout.connect(lambda: Enemies.move_bonus
                                        (self.health_bonus))
        self.main_timer.timeout.connect(lambda: Enemies.move_bonus
                                        (self.bullet_bonus))
        self.main_timer.timeout.connect(lambda: self.intersect_bonus_health())
        self.main_timer.timeout.connect(lambda: self.intersect_bonus_bullet())
        self.main_timer.timeout.connect(lambda: self.score.
                                        intersect_mystery_ship
                                        (self.bullets, self.mystery_ship))
        self.main_timer.timeout.connect(lambda: self.move_mystery_ship())
        self.main_timer.timeout.connect(lambda: self.mystery_ship.is_outside())
        self.main_timer.start(5)
        self.invaders_fire_timer = QtCore.QTimer()
        self.invaders_fire_timer.timeout.connect(
            lambda: self.invader_makes_bullets())
        self.invaders_fire_timer.start(Values.INTERVAL_FOR_INVADERS)
        self.score_timer = QtCore.QTimer()
        self.score_timer.timeout.connect(lambda: self.score.reduce())
        self.score_timer.start(Values.INTERVAL_FOR_SCORE)
        self.able_fire = False
        self.cart_fire_timer = QtCore.QTimer()
        self.cart_fire_timer.timeout.connect(lambda: self.able_to_fire())
        self.cart_fire_timer.start(self.level.interval_cart)
        self.mystery_timer = QtCore.QTimer()
        self.mystery_timer.timeout.connect(lambda: self.go_mystery_ship())
        self.mystery_timer.start(self.level.interval_mystery_ship)
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
        self.print_cart_lives(painter)
        if self.cart.lives <= 0:
            self.game_is_over = True
            self.print_game_over(painter)
        self.print_score(painter)
        self.print_pause(painter)
        self.print_health_bonus(painter)
        self.print_bullet_bonus(painter)
        self.print_mystery_ship(painter)
        self.print_scoreboard(painter)

    def stopTimers(self):
        if self.pause_mode or self.game_is_over or self.scoreboard_mode:
            self.main_timer.stop()
            self.invaders_fire_timer.stop()
            self.score_timer.stop()
            self.cart_fire_timer.stop()
            self.mystery_timer.stop()
        else:
            self.main_timer.start()
            self.invaders_fire_timer.start()
            self.score_timer.start()
            self.cart_fire_timer.start()
            self.mystery_timer.start()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_P or self.game_is_over:
            self.pause_mode = not self.pause_mode
            self.stopTimers()
        if not (self.pause_mode or self.game_is_over or self.scoreboard_mode):
            if key == QtCore.Qt.Key_Right:
                self.cart.move(Values.RIGHT)
                self.cart.direction = Values.RIGHT
            if key == QtCore.Qt.Key_Left:
                self.cart.move(Values.LEFT)
                self.cart.direction = Values.LEFT
            if key == QtCore.Qt.Key_Space and self.able_fire:
                angle = 360 + 60
                if (self.cart.x_left + self.cart.width // 2 >=
                        Values.WINDOW_WIDTH / 2):
                    angle = 60
                velocity = abs(self.cart.vx) * 0.2
                if self.cart.y_top >= 715:
                    angle = 90
                bullet = Enemies.CartBullet(self.cart.x_left,
                                            self.cart.y_top - 2,
                                            Values.BULLET_RADIUS,
                                            Values.BULLET_RADIUS, angle,
                                            velocity, 1 + self.addition_power)
                self.addition_power = 0
                self.bullets.append(bullet)
                self.cart_fire_timer.start(self.level.interval_cart)
                self.able_fire = False
        if key == QtCore.Qt.Key_S and self.saving_count < 3:
            self.saving.invaders = self.save_things(self.invaders)
            self.saving.invader_bullets = self.save_things(self.bullets_inv)
            self.saving.bullets = self.save_things(self.bullets)
            self.saving.score = self.score
            self.saving.cart = copy.deepcopy(self.cart)
            self.saving.bunkers = self.save_things(self.bunkers)
            self.saving.health_bonus = copy.deepcopy(self.health_bonus)
            self.saving.bullet_bonus = copy.deepcopy(self.bullet_bonus)
            self.saving.mystery_ship = copy.deepcopy(self.mystery_ship)
            self.saving_count += 1

        if (key == QtCore.Qt.Key_V and self.saving_count >= 1 and
                self.loading_count <= 2):
            self.cart = copy.deepcopy(self.saving.cart)
            self.score = copy.deepcopy(self.saving.score)
            self.invaders = copy.deepcopy(self.load_things
                                          (self.saving.invaders))
            self.bullets_inv = copy.deepcopy(self.load_things
                                             (self.saving.invader_bullets))
            self.bullets = copy.deepcopy(self.load_things(self.saving.bullets))
            self.bunkers = copy.deepcopy(self.load_things(self.saving.bunkers))
            self.health_bonus = copy.deepcopy(self.saving.health_bonus)
            self.bullet_bonus = copy.deepcopy(self.saving.bullet_bonus)
            self.mystery_ship = copy.deepcopy(self.saving.mystery_ship)
            self.mystery_timer.start()
            self.main_timer.start()
            self.cart_fire_timer.start()
            self.invaders_fire_timer.start()
            self.loading_count += 1

        if key == QtCore.Qt.Key_O:
            self.scoreboard_mode = not self.scoreboard_mode
            self.stopTimers()

    def win(self):
        if (len(self.invaders) == 0 and
                self.level_number != len(self.levels) - 1):
            self.saving = Enemies.Saving()
            self.saving_count = 0
            self.loading_count = 0
            self.level_number += 1
            self.level = Levels.levels(self.levels[self.level_number])
            self.bunkers = self.init_bunkers()
            self.invaders = self.init_invaders()
            self.cart = Enemies.Cart(470, 530, Values.CART_WIDTH,
                                     Values.CART_HEIGHT,
                                     self.level.weight_cart,
                                     self.level.lives_cart)

    def able_to_fire(self):
        self.able_fire = True

    def print_mystery_ship(self, painter):
        if self.mystery_ship.active:
            rect_ship = QtCore.QRect(self.mystery_ship.x_left,
                                     self.mystery_ship.y_top,
                                     self.mystery_ship.width,
                                     self.mystery_ship.height)
            painter.drawImage(rect_ship, Images.MYSTERY_SHIP)

    def print_bullet_bonus(self, painter):
        if self.bullet_bonus.active:
            rect_bullet_bonus = QtCore.QRect(self.bullet_bonus.x_left,
                                             self.bullet_bonus.y_top,
                                             self.bullet_bonus.width,
                                             self.bullet_bonus.height)
            painter.drawImage(rect_bullet_bonus, Images.BULLET_BONUS)

    def print_health_bonus(self, painter):
        if self.health_bonus.active:
            rect_health = QtCore.QRect(self.health_bonus.x_left,
                                       self.health_bonus.y_top,
                                       self.health_bonus.width,
                                       self.health_bonus.height)
            painter.drawImage(rect_health, Images.HEALTH)

    def print_score(self, painter):
        score = self.find_score()
        for i in range(5):
            rect_score = QtCore.QRect(1000 - 50 * i, 20, 50, 50)
            painter.drawImage(rect_score, Images.ARR[int(score[i])])

    def print_cart(self, painter):
        rect_cart = QtCore.QRect(self.cart.x_left, self.cart.y_top,
                                 self.cart.width, self.cart.height)
        if (self.cart.x_left + self.cart.width / 2 <=
                Values.WINDOW_WIDTH / 2 - 3):
            img = Images.CARTRD
            if self.cart.direction == Values.LEFT:
                img = Images.CARTLU
        else:
            img = Images.CARTLD
            if self.cart.direction == Values.RIGHT:
                img = Images.CARTRU
        painter.drawImage(rect_cart, img)

    def print_pause(self, painter):
        if self.pause_mode and not self.scoreboard_mode:
            rect_pause = QtCore.QRect(Values.WINDOW_WIDTH // 2 - 200,
                                      Values.WINDOW_HEIGHT // 2 - 200,
                                      400, 200)
            painter.drawImage(rect_pause, Images.PAUSE)

    def print_lives(self, painter, invader):
        rect_lives = QtCore.QRect(invader.x_left + 5,
                                  invader.y_top + invader.height,
                                  60, 5)
        full_value = self.level.lives[invader.level - 1]
        rect_our_lives = QtCore.QRect(invader.x_left + 5,
                                      invader.y_top + invader.height,
                                      int(invader.lives * 60 / full_value),
                                      5)
        painter.drawImage(rect_lives, Images.live_line)
        painter.drawImage(rect_our_lives, Images.line_full)

    def print_cart_lives(self, painter):
        painter.setFont(QtGui.QFont('XENOA', 30))
        rect_lives = QtCore.QRect(900, 750, 160, 60)
        rect_lives_width = min(self.cart.lives * 160 // self.level.lives_cart,
                               160)
        rect_our_lives = QtCore.QRect(900, 750, rect_lives_width, 60)
        painter.drawImage(rect_lives, Images.live_line)
        painter.drawImage(rect_our_lives, Images.line_full)
        painter.drawText(930, 795,
                         f'{self.cart.lives * 100 // self.level.lives_cart}%')

    def print_scoreboard(self, painter):
        if self.scoreboard_mode:
            rect_scoreboard = QtCore.QRect(Values.WINDOW_WIDTH // 2 - 300,
                                           Values.WINDOW_HEIGHT // 2 - 400,
                                           600, 800)
            painter.drawImage(rect_scoreboard, Images.SCOREBOARD)

    @staticmethod
    def print_bunker(painter, bunker):
        rect_bunker = QtCore.QRect(bunker.x_left, bunker.y_top,
                                   bunker.width, bunker.height)
        painter.drawImage(rect_bunker, Images.BUNKERS[bunker.lives - 1])

    @staticmethod
    def print_invaders(painter, invader):
        rect_invader = QtCore.QRect(invader.x_left, invader.y_top,
                                    invader.width, invader.height)
        painter.drawImage(rect_invader, Images.INVADERS[invader.level - 1])

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
                bullet.move()
                if bullet.y_top + bullet.height >= 850:
                    self.bullets.remove(bullet)

    def invader_makes_bullets(self):
        if not (self.game_is_over or len(self.invaders) <= 0 or
                self.pause_mode):
            invader = self.invaders[randint(0, len(self.invaders) - 1)]
            bullet = Enemies.InvaderBullet(invader.x_left, invader.y_top,
                                           Values.BULLET_RADIUS,
                                           Values.BULLET_RADIUS,
                                           self.cart, 1, invader.lives,
                                           self.level.types
                                           [invader.level - 1],
                                           invader)
            self.bullets_inv.append(bullet)

    def invader_fire(self):
        if not (self.game_is_over or self.pause_mode):
            for bullet in self.bullets_inv:
                bullet.move()
                if bullet.y_top + bullet.height >= 800:
                    self.bullets_inv.remove(bullet)

    def go_mystery_ship(self):
        self.mystery_ship = Enemies.MysteryShip(0, 50, 160, 80, self.bullets,
                                                True)

    def move_mystery_ship(self):
        if self.mystery_ship.active:
            self.mystery_ship.x_left += 1

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
                if (Values.CAN_MOVE_DOWN and
                        self.invaders[len(self.invaders) - 1].y_top < 350):
                    invader.move_down(step * 40)
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

    def intersect_bonus_health(self):
        if self.health_bonus.active:
            self.health_bonus.intersect_cart()

    def intersect_bonus_bullet(self):
        if self.bullet_bonus.active:
            self.addition_power = self.bullet_bonus.intersect_cart()

    def intersection_bullet_invader(self):
        for invader in self.invaders:
            invader.intersect_bullet(self.bullets, self.invaders)

    def game_over(self):
        return self.cart.lives <= 0

    def kill_bunker(self):
        for bunker in self.bunkers:
            bunker.bullet_intersection(self.bullets_inv, self.bunkers)

    def find_score(self):
        score_numbers = []
        for i in range(0, 5):
            score_numbers.append(self.score.score // 10 ** i % 10)
        return score_numbers

    def init_invaders(self):
        invaders = []
        easy1 = self.level.invadersEasyFirst
        easy2 = self.level.invadersEasySecond
        easy3 = self.level.invadersEasyThird
        medium1 = self.level.invadersMediumFirst
        medium2 = self.level.invadersMediumSecond
        medium3 = self.level.invadersMediumThird
        hard1 = self.level.invadersHardFirst
        hard2 = self.level.invadersHardSecond
        hard3 = self.level.invadersHardThird
        count1 = easy1 + medium1 + hard1
        count2 = easy2 + medium2 + hard2
        count3 = easy3 + medium3 + hard3
        self.append_invaders(count1, invaders, medium1, hard1, 0)
        self.append_invaders(count2, invaders, medium2, hard2, 1)
        self.append_invaders(count3, invaders, medium3, hard3, 2)
        return invaders

    def append_invaders(self, count, invaders, medium, hard, raw):
        hard_v = 3 if hard > 0 else -1
        mid_v = 2 if medium > 0 else -1
        easy_v = 1 if count - hard - medium > 0 else -1
        for i in range(count):
            invaders.append(Enemies.Invader(30 + (i % 6) * 150, 50 + 80 * raw,
                                            Values.INVADER_WIDTH,
                                            Values.INVADER_HEIGHT,
                                            self.level.lives
                                            [max(hard_v, mid_v, easy_v) - 1],
                                            max(hard_v, mid_v, easy_v)))
            hard -= 1
            if hard <= 0:
                hard_v = -1
                medium -= 1
            if medium <= 0:
                mid_v = -1

    @staticmethod
    def init_bunkers():
        bunkers = []
        for i in range(Values.BUNKERS_COUNT):
            bunkers.append(Enemies.Bunker((100 + (i + 1) * 350) % 900,
                                          430, 100, 100, 3))
        return bunkers

    def init_bonuses(self):
        for invader in self.invaders:
            for bullet in self.bullets:
                if Enemies.rectangles_intersected(bullet, invader):
                    random = randint(0, 100)
                    count = self.level.probability // 2
                    if 0 <= random < count:
                        self.health_bonus = Enemies.HealthBonus(invader.x_left,
                                                                invader.y_top,
                                                                40, 40,
                                                                self.cart,
                                                                self.level.
                                                                lives_bonus,
                                                                True)
                    if count <= random <= 2 * count:
                        self.bullet_bonus = Enemies.BulletBonus(invader.x_left,
                                                                invader.y_top,
                                                                40, 40,
                                                                self.cart,
                                                                self.level.
                                                                bullet_bonus,
                                                                True)

    @staticmethod
    def save_things(things):
        result = []
        for thing in things:
            result.append(copy.deepcopy(thing))
        return result

    @staticmethod
    def load_things(things):
        result = []
        for thing in things:
            result.append(copy.deepcopy(thing))
        return result


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SPACE INVADERS")
    window = MainWindow()
    sys.exit(app.exec_())

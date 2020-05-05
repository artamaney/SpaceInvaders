from math import sin, cos, pi
import Values
from random import randint


class Invader:
    def __init__(self, x, y, width, height, lives, level):
        if (x < 0 or x > Values.WINDOW_WIDTH or
                y < 0 or y > Values.WINDOW_HEIGHT or
                height < 10 or width < 10 or height > 100 or width > 200 or
                lives <= 0 or level > 3 or level <= 0):
            raise ValueError
        self.lives = lives
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.level = level

    def intersect_bullet(self, bullets, invaders):
        for bullet in bullets:
            if rectangles_intersected(bullet, self):
                self.lives -= 1
                if self.lives <= 0:
                    invaders.remove(self)
                bullets.remove(bullet)

    def move_right(self, step):
        self.x_left += step

    def move_down(self, step):
        self.y_top += step * 10

    def move_left(self, step):
        self.x_left -= step


def func_of_moving(x):
    return -abs(0.4 * x - 216) + 770


class Cart:
    def __init__(self, x, y, width, height, weight, lives):
        if (x < 0 or x > Values.WINDOW_WIDTH or
                y < 0 or y > Values.WINDOW_HEIGHT or
                height < 10 or width < 10 or lives <= 0 or
                height > 100 or width > 200 or weight <= 0):
            raise ValueError
        self.lives = lives
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.direction = 'LEFT'
        self.weight = weight

    def intersect_cart(self, bullets_invader):
        for bullet in bullets_invader:
            if rectangles_intersected(bullet, self):
                self.lives -= bullet.damage
                bullets_invader.remove(bullet)

    def move(self, direction, step_width):
        x_middle = self.x_left + self.width / 2
        real_step = 3 * step_width
        if x_middle < 540 and self.lives > 0:
            x_middle += step_width
            if direction == Values.RIGHT:
                x_middle += real_step
            if direction == Values.LEFT and self.x_left > 0 \
                    and self.x_left - 3 * step_width > 0:
                x_middle -= real_step
            y_middle = func_of_moving(x_middle)
            self.y_top = y_middle - self.height / 2
            self.x_left = x_middle - self.width / 2
        if x_middle >= Values.WINDOW_WIDTH / 2 and self.lives > 0:
            x_middle -= step_width
            if direction == Values.LEFT:
                x_middle -= real_step
            if direction == Values.RIGHT and \
                    self.x_left + self.width + real_step < Values.WINDOW_WIDTH:
                x_middle += real_step
            y_middle = func_of_moving(x_middle)
            self.y_top = y_middle - self.height / 2
            self.x_left = x_middle - self.width / 2


class Cart_Bullet:
    def __init__(self, x, y, width, height, angle):
        if width < 1 or width > 30 or height < 1 or height > 30:
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.angle = angle
        self.time = 0
        self.sign = -1 if angle <= 90 else 1

    def move(self, velocity):
        g = 10
        if self.x_left < 0:
            self.sign = 1
        if self.x_left > Values.WINDOW_WIDTH:
            self.sign = -1
        velocity_y = velocity * sin(self.angle / 360 * pi * 2) - g * self.time
        velocity_x = velocity * cos(self.angle / 360 * pi * 2) * self.sign
        self.x_left += velocity_x
        self.y_top -= velocity_y
        self.time += 0.001


class Invader_Bullet:
    def __init__(self, x, y, width, height, cart,
                 velocity, damage, type, invader):
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.damage = damage
        self.x1 = cart.x_left
        self.y1 = cart.y_top
        self.type = type
        self.invader = invader
        if type is Values.AIM_CART:
            self.step = (self.y1 - self.y_top) / (self.x1 - self.x_left)
            self.step = velocity / self.step
        if type is Values.BAD_AIM_CART:
            self.step = (self.y1 + randint(-100, 100) - self.y_top) \
                        / (self.x1 + randint(-100, 100) - self.x_left)
            self.step = velocity / self.step
        if type is Values.AIM_RANDOM:
            self.step = (randint(600, Values.WINDOW_HEIGHT) - self.y_top) \
                        / (randint(0, Values.WINDOW_WIDTH) - self.x_left)
            self.step = velocity / self.step

    def move(self):
        self.x_left += self.step
        self.y_top += 1


class Bunker:
    def __init__(self, x, y, width, height, lives):
        if width > 200 or width < 10 or height > 200 \
                or height < 10 or lives <= 0 or x < 5 or x > 1070 \
                or y < 400 or y > 800 or lives > 5:
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.lives = lives

    def bullet_intersection(self, bullets, bunkers):
        for bullet in bullets:
            if rectangles_intersected(bullet, self):
                self.lives -= 1
                self.height //= 2
                self.y_top += bullet.height
                bullets.remove(bullet)
                if self.lives == 0:
                    bunkers.remove(self)


class Score:
    def __init__(self, score):
        self.score = score

    def reduce(self):
        if self.score > 0:
            self.score -= 1

    def intersect_invader(self, bullets, invaders):
        for invader in invaders:
            for bullet in bullets:
                if rectangles_intersected(bullet, invader):
                    self.score += 50

    def intersect_cart(self, bullets, cart):
        for bullet in bullets:
            if rectangles_intersected(bullet, cart):
                self.score -= 1000 * bullet.damage // cart.lives
                if self.score < 0:
                    self.score = 0


def rectangles_intersected(r1, r2):
    return not (r1.y_top > r2.y_top + r2.height or
                r2.y_top > r1.y_top + r1.height or
                r1.x_left + r1.width < r2.x_left or
                r2.x_left + r2.width < r1.x_left)

from math import sin, cos, pi
import Values
from random import randint
from enum import Enum


class AttackType(Enum):
    AIM = 1
    AIM_AND_RANDOM = 2
    RANDOM = 3


class Invader:
    def __init__(self, x, y, width, height, lives, level):
        if not (0 <= x <= Values.WINDOW_WIDTH and
                0 <= y <= Values.WINDOW_HEIGHT and
                10 <= height <= 100 and 10 <= width <= 200 and
                lives > 0 and 0 < level <= 3):
            raise ValueError
        self.lives = lives
        self.full_lives = lives
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.level = level

    def intersect_bullet(self, bullets, invaders):
        for bullet in bullets:
            if rectangles_intersected(bullet, self):
                self.lives = max(0, self.lives - 1)
                bullet.power = max(0, bullet.power - 1)
                if bullet.power <= 0:
                    bullets.remove(bullet)
                if self.lives <= 0:
                    invaders.remove(self)

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
        if not (0 <= x <= Values.WINDOW_WIDTH and
                0 <= y <= Values.WINDOW_HEIGHT and
                10 <= height <= 100 and 10 <= width <= 200 and weight > 0):
            raise ValueError
        self.lives = lives
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.direction = Values.NOPE
        self.weight = weight
        self.vx = 0
        self.vy = 0
        self.sign = 1

    def move(self, direction):
        F = 0
        x_middle = self.x_left + self.width / 2
        sina = sin(pi / 6)
        cosa = cos(pi / 6)
        g = Values.G
        m = self.weight
        if direction == Values.LEFT:
            F = 10 if x_middle <= Values.WINDOW_WIDTH / 2 else -10
        elif direction == Values.RIGHT:
            F = -10 if x_middle <= Values.WINDOW_WIDTH / 2 else 10
        if x_middle <= Values.WINDOW_WIDTH / 2:
            self.sign = 1 if self.vx <= 0 else -1
        else:
            self.sign = -1 if self.vx < 0 else 1
        ma = (m * g * sina +
              Values.RATIO * m * g * cosa * self.sign - F)
        a = ma / m
        dx = a * cosa * 0.001
        if x_middle <= Values.WINDOW_WIDTH / 2:
            self.vx += dx
            if self.x_left <= 0:
                self.vx = 0.1
            if direction == Values.NOPE:
                x_middle += self.vx
            if direction == Values.LEFT and self.x_left > 0:
                x_middle += self.vx
            if direction == Values.RIGHT:
                x_middle += self.vx
        if x_middle > Values.WINDOW_WIDTH / 2:
            self.vx -= dx
            if self.x_left + self.width >= Values.WINDOW_WIDTH:
                self.vx = -0.1
            if direction == Values.NOPE:
                x_middle += self.vx
            if (direction == Values.RIGHT and
                    x_middle + self.width <= Values.WINDOW_WIDTH):
                x_middle += self.vx
            if direction == Values.LEFT:
                x_middle -= self.vx
        y_middle = func_of_moving(x_middle)
        self.y_top = y_middle - self.height / 2
        self.x_left = x_middle - self.width / 2
        if self.x_left <= Values.WINDOW_WIDTH / 2:
            self.x_left = max(x_middle - self.width / 2, 0)
        if self.x_left > Values.WINDOW_WIDTH - self.width:
            self.x_left = Values.WINDOW_WIDTH - self.width

    def intersect_cart(self, bullets_invader):
        for bullet in bullets_invader:
            if rectangles_intersected(bullet, self):
                self.lives = max(0, self.lives - bullet.damage)
                bullets_invader.remove(bullet)


class CartBullet:
    def __init__(self, x, y, width, height, angle, cart_force, power):
        if not (1 <= width <= 30 and 1 <= height <= 30 and power >= 1):
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.angle = angle
        self.time = 0
        self.cart_force = cart_force
        self.sign = -1 if angle <= 90 else 1
        self.velocity = 3
        self.power = power

    def move(self):
        g = Values.G
        if self.x_left < 0:
            self.sign = 1
        if self.x_left > Values.WINDOW_WIDTH:
            self.sign = -1
        velocity_y = self.velocity * sin(self.angle / 180 * pi) - g * self.time
        velocity_x = (self.velocity * cos(self.angle / 180 * pi) * self.sign +
                      self.cart_force * self.sign)
        self.x_left += velocity_x
        self.y_top -= velocity_y
        self.time += 0.001


class InvaderBullet:
    def __init__(self, x, y, width, height, cart,
                 velocity, damage, attack_type, invader):
        if not (1 <= width <= 30 and 1 <= height <= 30 and
                1 <= attack_type <= 3 and damage > 0 and velocity > 0):
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.damage = damage
        self.x1 = cart.x_left
        self.y1 = cart.y_top
        self.type = attack_type
        self.step = 0
        self.invader = invader
        if AttackType(self.type) == AttackType.AIM:
            self.step = (self.y1 - self.y_top) / (self.x1 - self.x_left)
            self.step = velocity / self.step
        if AttackType(self.type) == AttackType.AIM_AND_RANDOM:
            self.step = ((self.y1 + randint(-100, 100) - self.y_top) /
                         (self.x1 + randint(-100, 100) - self.x_left))
            self.step = velocity / self.step
        if AttackType(self.type) == AttackType.RANDOM:
            self.step = ((randint(600, Values.WINDOW_HEIGHT) - self.y_top) /
                         (randint(0, Values.WINDOW_WIDTH) - self.x_left))
            self.step = velocity / self.step

    def move(self):
        self.x_left += self.step
        self.y_top += 1


class Bunker:
    def __init__(self, x, y, width, height, lives):
        if not (10 <= width <= 200 and 10 <= height <= 200 and
                0 < lives <= 5 and 5 <= x <= Values.WINDOW_WIDTH - 10 and
                400 <= y <= Values.WINDOW_HEIGHT - 40):
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
    def __init__(self, score, mystery_score, fire_score):
        if score < 0:
            raise ValueError
        self.score = score
        self.mystery_score = mystery_score
        self.fire_score = fire_score

    def reduce(self):
        self.score = max(0, self.score - 1)

    def intersect_invader(self, bullets, invaders):
        for invader in invaders:
            for bullet in bullets:
                if rectangles_intersected(bullet, invader):
                    self.score += self.fire_score

    def intersect_cart(self, bullets, cart):
        for bullet in bullets:
            if rectangles_intersected(bullet, cart):
                self.score = max(0, self.score - 1000 *
                                 bullet.damage // cart.lives)
                break

    def intersect_mystery_ship(self, bullets, mystery_ship):
        if mystery_ship.active:
            for bullet in bullets:
                if rectangles_intersected(bullet, mystery_ship):
                    self.score += self.mystery_score
                    bullets.remove(bullet)
                    mystery_ship.active = False
                    mystery_ship.y_top = 2000
                    break


class HealthBonus:
    def __init__(self, x, y, width, height, cart, lives, active):
        if not (0 <= x <= Values.WINDOW_WIDTH and
                0 <= y <= Values.WINDOW_HEIGHT and 0 <= width <= 200 and
                0 <= height <= 200 and 0 <= lives <= 5):
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.cart = cart
        self.lives = lives
        self.active = active
        self.time = 0
        self.angle = -1
        self.sign = 1

    def intersect_cart(self):
        if self.active and rectangles_intersected(self.cart, self):
            self.cart.lives += self.lives
            self.active = False
            self.y_top = 2000

    def is_outside(self):
        if self.y_top >= Values.WINDOW_HEIGHT:
            self.active = False


class BulletBonus:
    def __init__(self, x, y, width, height, cart, power, active):
        if not (0 <= x <= Values.WINDOW_WIDTH and
                0 <= y <= Values.WINDOW_HEIGHT and 0 <= width <= 200 and
                0 <= height <= 200 and power >= 0):
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.cart = cart
        self.active = active
        self.power = power
        self.time = 0
        self.angle = -1
        self.sign = 1

    def intersect_cart(self):
        if self.active and rectangles_intersected(self.cart, self):
            self.active = False
            self.y_top = 2000
            return self.power
        return 0

    def is_outside(self):
        if self.y_top >= Values.WINDOW_HEIGHT:
            self.active = False


def move_bonus(bonus):
    if bonus.active:
        g = Values.G
        velocity = 0.1
        if bonus.angle == -1:
            bonus.angle = randint(45, 135)
        if bonus.x_left < 0:
            bonus.sign = 1
        if bonus.x_left > Values.WINDOW_WIDTH:
            bonus.sign = -1
        velocity_y = velocity * sin(bonus.angle / 180 * pi) + g * bonus.time
        velocity_x = 10 * velocity * cos(bonus.angle / 180 * pi) * bonus.sign
        bonus.x_left += velocity_x
        bonus.y_top += velocity_y
        bonus.time += 0.0005
        bonus.is_outside()


class MysteryShip:
    def __init__(self, x, y, width, height, bullets, active):
        if not (0 <= x <= Values.WINDOW_WIDTH and
                0 <= y <= Values.WINDOW_HEIGHT and
                0 <= width <= 300 and 0 <= height <= 200):
            raise ValueError
        self.x_left = x
        self.y_top = y
        self.width = width
        self.height = height
        self.bullets = bullets
        self.active = active

    def is_outside(self):
        if self.x_left >= Values.WINDOW_WIDTH:
            self.active = False


def rectangles_intersected(r1, r2):
    return (r2.y_top - r1.height <= r1.y_top <= r2.y_top + r2.height and
            r1.x_left - r2.width <= r2.x_left <= r1.x_left + r1.width)


class Saving:
    def __init__(self):
        self.invaders = []
        self.invader_bullets = []
        self.bullets = []
        self.score = 0
        self.cart = []
        self.bunkers = []
        self.health_bonus = []
        self.bullet_bonus = []
        self.mystery_ship = []

import unittest
import Enemies
import Values
import Levels
import configparser


class CartTests(unittest.TestCase):
    def test_cart_init_OK(self):
        cart = Enemies.Cart(50, 50, 50, 50, 50, 3)
        self.assertEqual(cart.x_left, 50)
        self.assertEqual(cart.y_top, 50)
        self.assertEqual(cart.width, 50)
        self.assertEqual(cart.height, 50)
        self.assertEqual(cart.weight, 50)
        self.assertEqual(cart.lives, 3)

    def test_cart_inside_window(self):
        self.cart = Enemies.Cart(50, 530, 100, 80, 1, 3)
        self.window_width = Values.WINDOW_WIDTH
        self.window_height = Values.WINDOW_HEIGHT
        for i in range(200):
            self.cart.move(Values.LEFT)
        self.assertGreaterEqual(self.cart.x_left, 0)
        self.assertGreaterEqual(self.cart.y_top, 0)
        self.assertGreaterEqual(840, self.cart.y_top)
        for i in range(400):
            self.cart.move(Values.RIGHT)
        self.assertGreaterEqual(1080, self.cart.x_left + self.cart.width)
        self.assertGreaterEqual(self.cart.y_top, 0)
        self.assertGreaterEqual(840, self.cart.y_top)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.incorrect_cart1 = Enemies.Cart(5, -9, 100, 80, 1, 3)
        with self.assertRaises(ValueError):
            self.incorrect_cart2 = Enemies.Cart(9999, 5, 0, 1, 2, 3)
        with self.assertRaises(ValueError):
            self.incorrect_cart3 = Enemies.Cart(0, 0, 0, 0, 0, 3)
        with self.assertRaises(ValueError):
            self.incorrect_cart4 = Enemies.Cart(0, 0, 9.9999, 9.9999, 0.001, 3)

    def test_cart_is_going_down(self):
        self.cart = Enemies.Cart(50, 530, 100, 80, 1, 3)
        for i in range(1000):
            self.cart.move(Values.NOPE)
        self.assertGreater(self.cart.x_left, 50)
        self.assertGreater(self.cart.y_top, 530)

    def test_cart_is_going_down_and_after_up_right(self):
        self.cart = Enemies.Cart(50, 530, 100, 80, 1, 3)
        for i in range(1000):
            self.cart.move(Values.NOPE)
        for i in range(10000):
            self.cart.move(Values.RIGHT)
        self.assertGreater(self.cart.x_left, Values.WINDOW_WIDTH // 2)
        self.assertGreater(Values.WINDOW_HEIGHT - 100, self.cart.y_top)


class BulletTests(unittest.TestCase):
    def test_init_is_OK(self):
        bullet = Enemies.CartBullet(55, 55, 5, 5, 90, 3, 1)
        self.assertEqual(bullet.x_left, 55)
        self.assertEqual(bullet.y_top, 55)
        self.assertEqual(bullet.width, 5)
        self.assertEqual(bullet.height, 5)
        self.assertEqual(bullet.angle, 90)

    def test_bullet_doesnt_know_about_negative_y(self):
        bullet = Enemies.CartBullet(1, 1, 1, 1, 90, 3, 1)
        bullet.move()  # it is illegal
        self.assertGreater(0, bullet.y_top)

    def test_bullet_bounce_after_wall(self):
        bullet = Enemies.CartBullet(0.5, 1, 1, 1, 45, 3, 1)
        bullet.move()
        bullet.move()
        bullet.move()
        self.assertGreater(bullet.x_left, 1)

    def test_bullet_moves_correctly(self):
        bullet1 = Enemies.CartBullet(1, 500, 1, 1, 90, 3, 1)
        bullet1.move()
        self.assertEqual(bullet1.y_top, 497)
        bullet2 = Enemies.CartBullet(10, 500, 1, 1, 30, 3, 1)
        bullet2.move()
        self.assertEqual(bullet2.y_top, 498.5)
        self.assertGreater(10, bullet2.x_left)
        bullet3 = Enemies.CartBullet(10, 500, 1, 1, 60, 3, 1)
        bullet3.move()
        bullet_x_moves_OK3 = 5.5 - 1e-5 <= bullet3.x_left <= 5.5 + 1e-5
        self.assertTrue(bullet_x_moves_OK3)
        self.assertGreater(500, bullet3.y_top)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.bullet = Enemies.CartBullet(1, 1, 0, 0, 60, 3, 1)
        with self.assertRaises(ValueError):
            self.bullet = Enemies.CartBullet(1, 1, -1, -1, 666, 999, 1)


class InvaderTests(unittest.TestCase):
    def test_init_OK(self):
        invader = Enemies.Invader(55, 55, 55, 55, 1, 1)
        self.assertEqual(invader.x_left, 55)
        self.assertEqual(invader.y_top, 55)
        self.assertEqual(invader.height, 55)
        self.assertEqual(invader.width, 55)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.invader = Enemies.Invader(1, 1, 0, 1, 1, 0)
        with self.assertRaises(ValueError):
            self.invader = Enemies.Invader(-1, 1, 1, 1, 1, 2)
        with self.assertRaises(ValueError):
            self.invader = Enemies.Invader(1, 1, 1, 1, 1, 4)
        with self.assertRaises(ValueError):
            self.invader = Enemies.Invader(555, 555, 555, 555, 99999999, 9999)


class BunkerTests(unittest.TestCase):
    def test_init_OK(self):
        bunker = Enemies.Bunker(51, 450, 50, 49, 1)
        self.assertEqual(bunker.x_left, 51)
        self.assertEqual(bunker.y_top, 450)
        self.assertEqual(bunker.width, 50)
        self.assertEqual(bunker.height, 49)
        self.assertEqual(bunker.lives, 1)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.bunker = Enemies.Bunker(-1, 450, 50, 50, 50)
        with self.assertRaises(ValueError):
            self.bunker = Enemies.Bunker(50, 450, 50, 50, -1)
        with self.assertRaises(ValueError):
            self.bunker = Enemies.Bunker(50, 450, 10000, 40000, 1)
        with self.assertRaises(ValueError):
            self.bunker = Enemies.Bunker(500, 450, 4, 4, 500000000000000)

    def test_intersection_OK(self):
        cart = Enemies.Cart(50, 50, 50, 50, 50, 3)
        bullets = [Enemies.InvaderBullet(50, 450, 25, 25, cart, 3, 3, 3, 0)]
        bunkers = [Enemies.Bunker(50, 450, 50, 50, 3)]
        for bunker in bunkers:
            bunker.bullet_intersection(bullets, bunkers)
        self.assertEqual(bunkers[0].lives, 2)


class ScoreTests(unittest.TestCase):
    def test_init_OK(self):
        score = Enemies.Score(0, 500, 50)
        self.assertEqual(score.score, 0)
        score = Enemies.Score(5000, 500, 50)
        self.assertEqual(score.score, 5000)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.score = Enemies.Score(-1, 500, 50)

    def test_reduce_OK(self):
        score = Enemies.Score(0, 500, 50)
        score.reduce()
        self.assertEqual(score.score, 0)
        score = Enemies.Score(500, 500, 50)
        for i in range(100):
            score.reduce()
        self.assertEqual(score.score, 400)

    def test_intersect_invader_OK(self):
        score = Enemies.Score(0, 500, 50)
        invaders = [Enemies.Invader(50, 50, 50, 50, 3, 1)]
        bullets = [Enemies.CartBullet(50, 50, 25, 25, 60, 3, 1)]
        score.intersect_invader(bullets, invaders)
        self.assertEqual(score.score, 50)

    def test_intersect_cart_OK(self):
        score = Enemies.Score(50, 500, 50)
        cart = Enemies.Cart(50, 50, 50, 50, 50, 3)
        bullets = [Enemies.InvaderBullet(50, 50, 25, 25, cart, 3, 3, 3, 0)]
        score.intersect_cart(bullets, cart)
        self.assertEqual(score.score, 0)


class HealthBonusTests(unittest.TestCase):
    def test_init_OK(self):
        bonus = Enemies.HealthBonus(0, 600, 60, 60,
                                    Enemies.Cart(50, 50, 50, 50, 50, 3), 3,
                                    True)
        self.assertEqual(0, bonus.x_left)
        self.assertEqual(600, bonus.y_top)
        self.assertEqual(60, bonus.width)
        self.assertEqual(60, bonus.height)
        self.assertEqual(3, bonus.lives)
        self.assertTrue(bonus.active)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.bonus = Enemies.HealthBonus(-1, 600, 60, 60,
                                             Enemies.Cart(50, 50, 50, 50,
                                                          50, 3), 3, True)
        with self.assertRaises(ValueError):
            self.bonus = Enemies.HealthBonus(0, 600, 560, 560,
                                             Enemies.Cart(50, 50, 50, 50, 50,
                                                          3), 3, True)
        with self.assertRaises(ValueError):
            self.bonus = Enemies.HealthBonus(0, 600, 60, 60,
                                             Enemies.Cart(50, 50, 50, 50, 50,
                                                          3), -6, True)

    def test_intersect_cart(self):
        bonus = Enemies.HealthBonus(50, 50, 60, 60,
                                    Enemies.Cart(50, 50, 50, 50, 50, 3),
                                    3, True)
        bonus.intersect_cart()
        self.assertEqual(6, bonus.cart.lives)


class BulletBonusTests(unittest.TestCase):
    def test_init_OK(self):
        bonus = Enemies.BulletBonus(0, 0, 100, 100,
                                    Enemies.Cart(50, 50, 50, 50, 50, 3),
                                    3, True)
        self.assertEqual(0, bonus.x_left)
        self.assertEqual(0, bonus.y_top)
        self.assertEqual(100, bonus.width)
        self.assertEqual(100, bonus.height)
        self.assertEqual(3, bonus.power)
        self.assertTrue(bonus.active)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.bonus = Enemies.BulletBonus(-1, 5, 5, 5, 5, 5, True)
        with self.assertRaises(ValueError):
            self.bonus = Enemies.BulletBonus(0, 0, 100, 100,
                                             Enemies.Cart(50, 50, 50,
                                                          50, 50, 3), -1, True)

    def test_intersect_cart(self):
        bonus = Enemies.BulletBonus(0, 0, 100, 100,
                                    Enemies.Cart(50, 50, 50, 50, 50, 3),
                                    3, True)
        add_power = bonus.intersect_cart()
        self.assertEqual(3, add_power)


class MysteryShipTests(unittest.TestCase):
    def test_init_OK(self):
        mystery_ship = Enemies.MysteryShip(0, 0, 100, 100, [Enemies.CartBullet
                                                            (0, 0, 25,
                                                             25, 60, 3, 1)],
                                           True)
        self.assertEqual(0, mystery_ship.x_left)
        self.assertEqual(0, mystery_ship.y_top)
        self.assertEqual(100, mystery_ship.width)
        self.assertEqual(100, mystery_ship.height)
        self.assertTrue(mystery_ship.active)

    def test_init_error(self):
        with self.assertRaises(ValueError):
            self.mystery_ship = Enemies.MysteryShip(-1, 0, 100, 100,
                                                    [Enemies.CartBullet
                                                     (0, 0, 25,
                                                      25, 60, 3, 1)],
                                                    True)
        with self.assertRaises(ValueError):
            self.mystery_ship = Enemies.MysteryShip(0, 0, 500, 900,
                                                    [Enemies.CartBullet
                                                     (0, 0, 25,
                                                      25, 60, 3, 1)],
                                                    True)

    def test_is_outside(self):
        mystery_ship = Enemies.MysteryShip(Values.WINDOW_WIDTH, 0, 100, 100,
                                           [Enemies.CartBullet(0, 0, 25, 25,
                                                               60, 3, 1)],
                                           True)
        mystery_ship.x_left += 1
        mystery_ship.is_outside()
        self.assertFalse(mystery_ship.active)


class LevelTests(unittest.TestCase):
    def test_init_OK(self):
        level = Levels.levels('leveltest.txt')
        self.assertEqual(level.hard_lives, 1)
        self.assertEqual(level.bullet_bonus, 1)
        self.assertEqual(level.probability, 1)
        self.assertEqual(level.angle_cart, 1)
        self.assertEqual(level.hard_damage, 1)
        self.assertEqual(level.hardInvadersCount, 6)

    def test_init_error(self):
        with self.assertRaises(configparser.NoSectionError):
            self.level = Levels.levels('something')


if __name__ == '__main__':
    unittest.main()

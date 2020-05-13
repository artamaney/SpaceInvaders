import configparser


class levels:
    def __init__(self, level):
        self.level = level
        config = configparser.ConfigParser()
        config.read(self.level)
        self.easy_damage = int(config.get('easyinvader', 'damage'))
        self.easy_lives = int(config.get('easyinvader', 'lives'))
        self.easy_type = int(config.get('easyinvader', 'type'))
        self.medium_damage = int(config.get('mediuminvader', 'damage'))
        self.medium_lives = int(config.get('mediuminvader', 'lives'))
        self.medium_type = int(config.get('mediuminvader', 'type'))
        self.hard_damage = int(config.get('hardinvader', 'damage'))
        self.hard_lives = int(config.get('hardinvader', 'lives'))
        self.hard_type = int(config.get('hardinvader', 'type'))
        self.easyInvadersCount = int(config.get('enemies',
                                                'easyInvadersCount'))
        self.mediumInvadersCount = int(config.get('enemies',
                                                  'mediumInvadersCount'))
        self.hardInvadersCount = int(config.get('enemies',
                                                'hardInvadersCount'))
        self.weight_cart = int(config.get('level', 'weight_cart')) * 0.01
        self.angle_cart = int(config.get('level', 'angle_cart'))
        self.interval_cart = int(config.get('level', 'interval_cart'))
        self.lives_cart = int(config.get('level', 'lives_cart'))
        self.probability = int(config.get('level', 'probability'))
        self.lives_bonus = int(config.get('level', 'lives_bonus'))
        self.bullet_bonus = int(config.get('level', 'bullet_bonus'))
        self.interval_mystery_ship = int(config.get('level',
                                                    'interval_mystery_ship'))
        self.lives = [self.easy_lives, self.medium_lives, self.hard_lives]
        self.types = [self.easy_type, self.medium_type, self.hard_type]
        self.damages = [self.easy_damage,
                        self.medium_damage,
                        self.hard_damage]

import configparser


def our_config_get(config, option, name):
    return int(config.get(option, name))


class levels:
    def __init__(self, level):
        self.level = level
        config = configparser.ConfigParser()
        config.read(self.level)
        self.easy_damage = our_config_get(config, 'easyinvader', 'damage')
        self.easy_lives = our_config_get(config, 'easyinvader', 'lives')
        self.easy_type = our_config_get(config, 'easyinvader', 'type')
        self.medium_damage = our_config_get(config, 'mediuminvader', 'damage')
        self.medium_lives = our_config_get(config, 'mediuminvader', 'lives')
        self.medium_type = our_config_get(config, 'mediuminvader', 'type')
        self.hard_damage = our_config_get(config, 'hardinvader', 'damage')
        self.hard_lives = our_config_get(config, 'hardinvader', 'lives')
        self.hard_type = our_config_get(config, 'hardinvader', 'type')
        self.easyInvadersCount = our_config_get(config, 'enemies',
                                                'easyInvadersCount')
        self.mediumInvadersCount = our_config_get(config, 'enemies',
                                                  'mediumInvadersCount')
        self.hardInvadersCount = our_config_get(config, 'enemies',
                                                'hardInvadersCount')
        self.weight_cart = our_config_get(config, 'level',
                                          'weight_cart') * 0.01
        self.angle_cart = our_config_get(config, 'level', 'angle_cart')
        self.interval_cart = our_config_get(config, 'level', 'interval_cart')
        self.lives_cart = our_config_get(config, 'level', 'lives_cart')
        self.probability = our_config_get(config, 'level', 'probability')
        self.lives_bonus = our_config_get(config, 'level', 'lives_bonus')
        self.bullet_bonus = our_config_get(config, 'level', 'bullet_bonus')
        self.interval_mystery_ship = our_config_get(config, 'level',
                                                    'interval_mystery_ship')
        self.mystery_ship_score = our_config_get(config, 'level',
                                                 'mystery_ship_score')
        self.fire_score = our_config_get(config, 'level',
                                         'fire_score')
        self.lives = [self.easy_lives, self.medium_lives, self.hard_lives]
        self.types = [self.easy_type, self.medium_type, self.hard_type]
        self.damages = [self.easy_damage,
                        self.medium_damage,
                        self.hard_damage]

import configparser


def our_config_get(config, option, name):
    return int(config.get(option, name))


def search_counts(config, option, name):
    try:
        return our_config_get(config, option, name)
    except configparser.NoOptionError:
        return 0


class levels:
    def __init__(self, level):
        self.level = level
        config = configparser.ConfigParser()
        config.read(self.level)

        '''ENEMIES'''
        self.easy_damage = our_config_get(config, 'easyinvader', 'damage')
        self.easy_lives = our_config_get(config, 'easyinvader', 'lives')
        self.easy_type = our_config_get(config, 'easyinvader', 'type')
        self.medium_damage = our_config_get(config, 'mediuminvader', 'damage')
        self.medium_lives = our_config_get(config, 'mediuminvader', 'lives')
        self.medium_type = our_config_get(config, 'mediuminvader', 'type')
        self.hard_damage = our_config_get(config, 'hardinvader', 'damage')
        self.hard_lives = our_config_get(config, 'hardinvader', 'lives')
        self.hard_type = our_config_get(config, 'hardinvader', 'type')

        self.invadersEasyFirst = search_counts(config, 'first_row_enemies',
                                               'easy')
        self.invadersEasySecond = search_counts(config, 'second_row_enemies',
                                                'easy')
        self.invadersEasyThird = search_counts(config, 'third_row_enemies',
                                               'easy')
        self.invadersMediumFirst = search_counts(config, 'first_row_enemies',
                                                 'medium')
        self.invadersMediumSecond = search_counts(config, 'second_row_enemies',
                                                  'medium')
        self.invadersMediumThird = search_counts(config, 'third_row_enemies',
                                                 'medium')
        self.invadersHardFirst = search_counts(config, 'first_row_enemies',
                                               'hard')
        self.invadersHardSecond = search_counts(config, 'second_row_enemies',
                                                'hard')
        self.invadersHardThird = search_counts(config, 'third_row_enemies',
                                               'hard')

        '''BONUSES'''
        self.bonuses = []
        number = 1
        while True:
            try:
                self.bonuses.append(config[f'bonus{number}'])
            except KeyError:
                break
            number += 1

        '''LEVEL'''
        self.weight_cart = our_config_get(config, 'level',
                                          'weight_cart') * 0.01
        self.interval_cart = our_config_get(config, 'level', 'interval_cart')
        self.lives_cart = our_config_get(config, 'level', 'lives_cart')
        self.interval_mystery_ship = our_config_get(config, 'level',
                                                    'interval_mystery_ship')
        self.mystery_ship_score = our_config_get(config, 'level',
                                                 'mystery_ship_score')
        self.fire_score = our_config_get(config, 'level', 'fire_score')

        self.lives = [self.easy_lives, self.medium_lives, self.hard_lives]
        self.types = [self.easy_type, self.medium_type, self.hard_type]
        self.damages = [self.easy_damage, self.medium_damage, self.hard_damage]

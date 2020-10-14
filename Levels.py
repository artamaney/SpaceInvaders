import configparser
# from multidict import MultiDict


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
        config.read(level)
        enemies = {}
        cnf = dict(config)
        for enemy in cnf:
            if enemy == 'DEFAULT':
                continue
            if enemy.startswith('enemy'):
                enemies[enemy] = cnf[enemy]
            else:
                break
        self.bonuses = []
        number = 1
        while True:
            try:
                self.bonuses.append(config[f'bonus{number}'])
            except KeyError:
                break
            number += 1
        self.invaders = []
        invaders_count = cnf['enemies']
        for enemy in invaders_count:
            self.invaders.append((enemies[f'enemy.{enemy}'],
                                 invaders_count[enemy]))
        self.weight_cart = our_config_get(config, 'level',
                                          'weight_cart') * 0.01
        self.interval_cart = our_config_get(config, 'level', 'interval_cart')
        self.lives_cart = our_config_get(config, 'level', 'lives_cart')
        self.interval_mystery_ship = our_config_get(config, 'level',
                                                    'interval_mystery_ship')
        self.mystery_ship_score = our_config_get(config, 'level',
                                                 'mystery_ship_score')
        self.fire_score = our_config_get(config, 'level', 'fire_score')

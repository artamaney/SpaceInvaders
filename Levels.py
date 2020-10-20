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
        config = configparser.ConfigParser(dict_type=my_dict, strict=False)
        self.enemies = {}
        self.bonuses = {}
        self.invaders = []
        level = {}
        config.read(self.level)
        sections = config._sections
        for section in sections:
            if section.startswith('enemy'):
                self.enemies[section] = dict(sections[section])
            elif section.startswith('bonus'):
                self.bonuses[section] = dict(sections[section])
            elif section.startswith('enemies'):
                items = sections[section].my_values
                for i in range(len(items)):
                    self.invaders.append((items[i][0], int(items[i][1][0])))
            elif section.startswith('level'):
                level = dict(sections[section])
        self.weight_cart = int(level['weight_cart'][0]) * 0.01
        self.interval_cart = int(level['interval_cart'][0])
        self.lives_cart = int(level['lives_cart'][0])
        self.interval_mystery_ship = int(level['interval_mystery_ship'][0])
        self.mystery_ship_score = int(level['mystery_ship_score'][0])
        self.fire_score = int(level['fire_score'][0])


class my_dict:
    def __init__(self):
        self.my_values = []

    def items(self):
        return [(None, my_dict())]

    def keys(self):
        keys = []
        for i in range(len(self.my_values)):
            keys.append(self.my_values[i][0])
        return keys

    def __setitem__(self, key, value):
        self.my_values.append((key, value))

    def __getitem__(self, item):
        for i in range(len(self.my_values)):
            if self.my_values[i][0] == item:
                return self.my_values[i][1]

    def __iter__(self):
        return iter(self.keys())

    def __get__(self, key, default=None):
        for i in range(len(self.my_values)):
            if self.my_values[i][0] == key:
                return self.my_values[i][1]
        return default

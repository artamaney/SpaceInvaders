import re


class levels:
    def __init__(self, level):
        self.level = level
        self.reg_exp = re.compile(r'(\d+)')
        self.easy_damage = 0
        self.easy_lives = 0
        self.easy_type = 0
        self.medium_damage = 0
        self.medium_lives = 0
        self.medium_type = 0
        self.hard_damage = 0
        self.hard_lives = 0
        self.hard_type = 0
        self.easyInvadersCount = 0
        self.mediumInvadersCount = 0
        self.hardInvadersCount = 0
        self.weight_cart = 0
        self.angle_cart = 0
        self.interval_cart = 0
        self.lives_cart = 0
        self.lives = [self.easy_lives, self.medium_lives, self.hard_lives]
        self.types = [self.easy_type, self.medium_type, self.hard_type]
        self.damages = [self.easy_damage,
                        self.medium_damage,
                        self.hard_damage]

    def parse_level(self):
        with open(f'level{self.level}.txt') as f:
            txt = f.read()
            groups = self.reg_exp.findall(txt)
            self.easy_damage = int(groups[0])
            self.easy_lives = int(groups[1])
            self.easy_type = int(groups[2])
            self.medium_damage = int(groups[3])
            self.medium_lives = int(groups[4])
            self.medium_type = int(groups[5])
            self.hard_damage = int(groups[6])
            self.hard_lives = int(groups[7])
            self.hard_type = int(groups[8])
            self.easyInvadersCount = int(groups[9])
            self.mediumInvadersCount = int(groups[10])
            self.hardInvadersCount = int(groups[11])
            self.weight_cart = int(groups[12]) * 0.01
            self.angle_cart = int(groups[13])
            self.interval_cart = int(groups[14])
            self.lives_cart = int(groups[15])
            self.lives = [self.easy_lives, self.medium_lives, self.hard_lives]
            self.types = [self.easy_type, self.medium_type, self.hard_type]
            self.damages = [self.easy_damage,
                            self.medium_damage,
                            self.hard_damage]
            f.close()

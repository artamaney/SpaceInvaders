class levels:
    def __init__(self, level):
        self.level = level

    def parse_level(self):
        with open(f'level{self.level}.txt') as f:
            txt = f.read()
            txt = txt.split('\n')
            for i in range(len(txt)):
                txt[i] = txt[i].split('=')[1]
            f.close()
            return txt

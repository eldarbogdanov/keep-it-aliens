import random

from clubsandwich.geom import Size

from constants import SPACESHIP_OFFSET


class Enemy(object):
    def __init__(self, char):
        self.id = random.randint(1, 100000)
        self.char = char
        self.size = Size(10, 8)
        self.speed = 0.2

    @classmethod
    def random(cls):
        return Enemy(chr(SPACESHIP_OFFSET + random.randint(0, 2)))

    def __repr__(self):
        return str(self.id)

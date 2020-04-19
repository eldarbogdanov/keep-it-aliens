import random

from clubsandwich.geom import Size, Point

from utils import VEHICLE_OFFSET_5x4, VEHICLE_OFFSET_6x5, BATTLE_WIDTH, COMMAND_SHIP_OFFSET


class Enemy(object):
    def __init__(self, char, size, hp, behavior, score, speed, deadly=False):
        self.id = random.randint(1, 100000)
        self.char = char
        self.hp = hp
        self.size = size
        self.behavior = behavior
        self.speed = speed
        self.deadly = deadly
        self.score = score

        self.streak = None

    def next_move(self, current_point):
        if self.behavior == "down":
            return Point(0, self.speed)
        if self.behavior == "random":
            if self.streak:
                ret = self.streak["point"]
                # don't let it go beyond battlefield bounds
                if current_point.x < 1 and ret.x < 0 or current_point.x > BATTLE_WIDTH - 1 - self.size.width and ret.x > 0:
                    self.streak = None
                    return Point(self.speed * (1 if current_point.x < 1 else -1), self.speed)
                if self.streak["moves"] == 1:
                    self.streak = None
                else:
                    self.streak["moves"] -= 1
                return ret
            else:
                # move in a specific direction for a random duration
                self.streak = {
                    "moves": random.randint(10, 50),
                    "point": Point(random.randint(-1, 1) * self.speed, self.speed)
                }
                return self.streak["point"]
        assert False, "Don't know this behavior: {}".format(self.behavior)

    def __repr__(self):
        return str(self.id)


fast_dropper_prototype = Enemy(chr(VEHICLE_OFFSET_5x4 + 0), Size(10, 8), 1, "down", 2, 0.3)
random_prototype = Enemy(chr(VEHICLE_OFFSET_5x4 + 1), Size(10, 8), 1, "random", 2, 0.2)
dropper_prototype = Enemy(chr(VEHICLE_OFFSET_5x4 + 2), Size(10, 8), 1, "down", 1, 0.2)
strong_random_prototype = Enemy(chr(VEHICLE_OFFSET_6x5), Size(12, 10), 2, "random", 3, 0.2)
strong_dropper_prototype = Enemy(chr(VEHICLE_OFFSET_6x5 + 1), Size(12, 10), 2, "down", 2, 0.2)
dreadnought_prototype = Enemy(chr(VEHICLE_OFFSET_6x5 + 2), Size(12, 10), 3, "random", 5, 0.25)
command_ship_prototype = Enemy(chr(COMMAND_SHIP_OFFSET), Size(18, 14), 10, "random", 100, 0.2, deadly=True)

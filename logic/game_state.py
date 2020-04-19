import copy
import random

from clubsandwich.geom import Point, Rect

from utils import SCREEN_HEIGHT, SCREEN_WIDTH, BATTLE_HEIGHT, BATTLE_WIDTH, ALIEN_FINISH, PLAYER_SPEED
from logic.enemies import dropper_prototype, random_prototype, fast_dropper_prototype, strong_dropper_prototype, \
    strong_random_prototype, dreadnought_prototype

FIRE_LAG = 40
FRAMES_PER_LEVEL = 10 * 60


class GameState(object):
    def __init__(self):
        self.level = 0
        self.living_enemies = None
        self.bullets = None
        self.next_available_fire = None
        self.escaped_enemies = None
        self.escaped_enemies_limit = None
        self.counter = None
        self.frames_left = None
        self.player_pos = None
        self.advance_to_next_level()

    def advance_to_next_level(self):
        self.level += 1
        self.living_enemies = []
        self.bullets = []
        self.next_available_fire = 0
        self.escaped_enemies = 0
        self.escaped_enemies_limit = 10
        self.counter = 0
        self.frames_left = FRAMES_PER_LEVEL
        self.player_pos = Point(BATTLE_WIDTH / 2, BATTLE_HEIGHT - 10)

    def level_name(self):
        if self.level == 1:
            return "San Francisco"
        if self.level == 2:
            return "New York"
        if self.level == 3:
            return "Washington, DC"

    def allowed_enemies(self):
        if self.level == 1:
            return [dropper_prototype, random_prototype, fast_dropper_prototype]
        if self.level == 2:
            return [fast_dropper_prototype, strong_dropper_prototype, strong_random_prototype]
        if self.level == 3:
            return [strong_dropper_prototype, strong_random_prototype, dreadnought_prototype]

    def _check_bullet_enemy_collision(self):
        # returns the set of destroyed enemies, modifies self.bullets
        new_bullets = []
        destroyed_enemies = set()
        for pos, speed in self.bullets:
            # might implement proper collision detection if needed
            new_pos = pos + speed
            mid_pos = (pos + new_pos) / 2
            used = False
            for enemy, enemy_pos in self.living_enemies:
                enemy_rect = Rect(origin=enemy_pos, size=enemy.size)
                if enemy_rect.contains(pos) or enemy_rect.contains(mid_pos) or enemy_rect.contains(new_pos):
                    print("Bullet at pos {}, new_pos {} destroyed enemy {}".format(pos, new_pos, enemy_rect))
                    destroyed_enemies.add(enemy)
                    used = True
            if not used and new_pos.y >= 0:
                new_bullets.append((pos, speed))
        self.bullets = new_bullets
        self.living_enemies = [(enemy, pos) for enemy, pos in self.living_enemies if enemy not in destroyed_enemies]
        return destroyed_enemies

    def process_one_frame(self):
        self.counter += 1
        self.frames_left -= 1
        new_living_enemies = []
        destroyed_enemies = self._check_bullet_enemy_collision()

        for enemy, pos in self.living_enemies:
            new_pos = pos + enemy.next_move(pos)
            if new_pos.y >= ALIEN_FINISH:
                self.escaped_enemies += 1
            else:
                new_living_enemies.append((enemy, new_pos))
        self.living_enemies = new_living_enemies

        destroyed_enemies.update(self._check_bullet_enemy_collision())

        self.bullets = [(pos + speed, speed) for pos, speed in self.bullets if self.is_valid_position(pos)]

        add_enemy = random.randint(1, 80) == 1
        if add_enemy:
            self._add_enemy()

        return destroyed_enemies

    def is_valid_position(self, pos):
        return pos.x >= 0 and pos.x < SCREEN_WIDTH and pos.y >= 0 and pos.y < SCREEN_HEIGHT

    def fire(self, dx, dy):
        if self.next_available_fire > self.counter:
            return False
        self.bullets.append((self.player_pos, Point(dx, dy)))
        self.next_available_fire += FIRE_LAG

    def move_left(self):
        self.player_pos = self.player_pos + Point(-PLAYER_SPEED, 0)

    def move_right(self):
        self.player_pos = self.player_pos + Point(PLAYER_SPEED, 0)

    def _add_enemy(self):
        type = copy.deepcopy(random.choice(self.allowed_enemies()))
        candidates = []
        for x in range(SCREEN_WIDTH - type.size.width):
            proposed_rect = Rect(origin=Point(x, 0), size=type.size)
            good = True
            for enemy, pos in self.living_enemies:
                enemy_rect = Rect(origin=pos, size=enemy.size)
                if proposed_rect.intersects(enemy_rect):
                    good = False
            if good:
                candidates.append(x)
        if candidates:
            x = random.choice(candidates)
            self.living_enemies.append((type, Point(x, 0)))

    def finished(self):
        return self.frames_left <= 0

    def lost(self):
        return self.escaped_enemies > self.escaped_enemies_limit

import copy
import random

from clubsandwich.geom import Point, Rect

from utils import BATTLE_HEIGHT, BATTLE_WIDTH, ALIEN_FINISH, PLAYER_SPEED, VEHICLE_OFFSET_5x4, BULLET_SPEED
from logic.enemies import dropper_prototype, random_prototype, fast_dropper_prototype, strong_dropper_prototype, \
    strong_random_prototype, dreadnought_prototype, command_ship_prototype

FIRE_LAG = 20
FPS = 72
FRAMES_PER_LEVEL = FPS * 20
FINAL_BOSS_FRAMES_LEFT = FPS * 6

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
        self.frames_left = 5 if self.level < 3 else FRAMES_PER_LEVEL
        self.player_pos = self.starting_position()

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
            return [dropper_prototype, strong_dropper_prototype, strong_random_prototype]
        if self.level == 3:
            return [strong_dropper_prototype, strong_random_prototype, dreadnought_prototype]

    def player_char(self):
        return chr(VEHICLE_OFFSET_5x4 + self.level + 2)

    def starting_position(self):
        if self.level == 1:
            return Point(BATTLE_WIDTH / 2, BATTLE_HEIGHT - 14)
        if self.level == 2:
            return Point(BATTLE_WIDTH / 2, BATTLE_HEIGHT - 9)
        return Point(BATTLE_WIDTH / 2, BATTLE_HEIGHT - 9)

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
                    enemy.hp -= 1
                    if enemy.hp <= 0:
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
                if enemy.deadly:
                    self.escaped_enemies += 100
            else:
                new_living_enemies.append((enemy, new_pos))
        self.living_enemies = new_living_enemies

        destroyed_enemies.update(self._check_bullet_enemy_collision())

        self.bullets = [(pos + speed, speed) for pos, speed in self.bullets if self.is_valid_position(pos)]

        # increase the chance as time passes?
        add_enemy = random.randint(1, 80) == 1
        if add_enemy:
            self._add_enemy()

        if self.level == 3 and self.frames_left == FINAL_BOSS_FRAMES_LEFT:
            self.living_enemies.append((command_ship_prototype, Point(BATTLE_WIDTH / 2, 0)))

        return destroyed_enemies

    def is_valid_position(self, pos):
        return pos.x >= 0 and pos.x < BATTLE_WIDTH and pos.y >= 0 and pos.y < BATTLE_HEIGHT

    def _inner_fire(self, dx, dy):
        if self.next_available_fire > self.counter:
            return False
        self.bullets.append((self.player_pos + Point(4, 0), Point(dx, dy)))
        self.next_available_fire += FIRE_LAG

    def fire(self):
        self._inner_fire(0, -BULLET_SPEED)

    def fire_left(self):
        self._inner_fire(-BULLET_SPEED / 2, -BULLET_SPEED)

    def fire_right(self):
        self._inner_fire(BULLET_SPEED / 2, -BULLET_SPEED)

    def move_left(self):
        self.player_pos = self.player_pos + Point(-PLAYER_SPEED, 0)

    def move_right(self):
        self.player_pos = self.player_pos + Point(PLAYER_SPEED, 0)

    def _add_enemy(self):
        type = copy.deepcopy(random.choice(self.allowed_enemies()))
        candidates = []
        for x in range(BATTLE_WIDTH - type.size.width):
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

import random

from clubsandwich.ui import View, Point, Rect

from utils import BATTLE_HEIGHT, BATTLE_WIDTH

bullet = """XXX
XXX
XXX"""


class GameView(View):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        self.have_drawn = 0
        super().__init__(*args, **kwargs)

    def draw(self, ctx):
        # for some reason the first time this is invoked, it doesn't render the background as expected
        if self.have_drawn < 2:
            ctx.layer(0)
            ctx.clear_area(self.bounds)
            ctx.print(Point(0, 0), chr(0x1000 * self.game_state.level))
            self.have_drawn += 1

        self.game_state.process_one_frame()

        ctx.layer(1)
        ctx.clear_area(self.bounds)

        ctx.color("white")
        for enemy, pos in self.game_state.living_enemies:
            ctx.print(self.rounded_point(pos), enemy.char)
        ctx.color("red")
        for pos, _ in self.game_state.bullets:
            ctx.print(self.rounded_point(pos), bullet)

    def rounded_point(self, point):
        return Point(round(point.x), round(point.y))

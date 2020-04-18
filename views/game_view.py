import random

from clubsandwich.ui import View, Point, Rect

from constants import BATTLE_HEIGHT, BATTLE_WIDTH

bullet = """XXX
XXX
XXX"""

class GameView(View):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        self.have_drawn = False
        super().__init__(*args, **kwargs)

    def draw(self, ctx):
        self.game_state.process_one_frame()
        if not self.have_drawn:
            ctx.layer(0)
            ctx.print(Point(0, 0), chr(0x1000 * self.game_state.level))
            self.have_drawn = True

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

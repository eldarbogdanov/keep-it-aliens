from clubsandwich.ui import UIScene, terminal, WindowView, LayoutOptions

from constants import BULLET_SPEED, SCREEN_WIDTH, BATTLE_WIDTH
from logic.game_state import GameState
from views.game_view import GameView


import cProfile

from views.info_view import InfoView

pr = cProfile.Profile()
pr.enable()


class GameScene(UIScene):
    def __init__(self, *args, **kwargs):
        self.game_state = GameState()
        self.info_view = InfoView(self.game_state)
        views = [
            GameView(self.game_state),
            WindowView(
                "",
                subviews=[self.info_view],
                layout_options=LayoutOptions.column_right(SCREEN_WIDTH - BATTLE_WIDTH)
            )
        ]
        super().__init__(views=views, *args, **kwargs)

    def terminal_read(self, val):
        if val == terminal.TK_LEFT:
            self.game_state.move_left()
        if val == terminal.TK_RIGHT:
            self.game_state.move_right()
        if val == terminal.TK_A:
            self.game_state.fire(-BULLET_SPEED, -BULLET_SPEED)
        if val == terminal.TK_S:
            self.game_state.fire(0, -BULLET_SPEED)
        if val == terminal.TK_D:
            self.game_state.fire(BULLET_SPEED, -BULLET_SPEED)
        if val == terminal.TK_ESCAPE:
            pr.dump_stats("profile")

    def terminal_update(self, is_active=False):
        super().terminal_update()
        # if self.game_state.finished():
        #     self.director.replace_scene(...)
        self.info_view.update()
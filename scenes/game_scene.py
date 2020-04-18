from clubsandwich.ui import UIScene, terminal

from logic.game_state import GameState
from views.game_view import GameView


import cProfile
pr = cProfile.Profile()
pr.enable()


class GameScene(UIScene):
    def __init__(self, *args, **kwargs):
        self.game_state = GameState()
        views = [
            GameView(self.game_state)
        ]
        super().__init__(views=views, *args, **kwargs)

    def terminal_read(self, val):
        if val == terminal.TK_LEFT:
            self.game_state.move_left()
        if val == terminal.TK_RIGHT:
            self.game_state.move_right()
        if val == terminal.TK_SPACE:
            self.game_state.fire(0, -1)
        if val == terminal.TK_ESCAPE:
            pr.dump_stats("profile")

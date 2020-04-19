from clubsandwich.ui import UIScene, terminal, WindowView, LayoutOptions, LabelView, ButtonView

import stories
import utils
from utils import BULLET_SPEED, SCREEN_WIDTH, BATTLE_WIDTH
from logic.game_state import GameState
from views.game_view import GameView


import cProfile

from views.info_view import InfoView

pr = cProfile.Profile()
pr.enable()

controls = """
Movement:
Left/Right

Shooting:
A, S, D
"""


class GameScene(UIScene):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        self.info_view = InfoView(self.game_state)
        controls_view = LabelView(
            utils.translate_text(controls),
            align_horz="left",
            layout_options=LayoutOptions.column_right(SCREEN_WIDTH - BATTLE_WIDTH - 2).with_updates(top=50)
        )
        views = [
            GameView(self.game_state),
            WindowView(
                "",
                subviews=[self.info_view],
                layout_options=LayoutOptions.column_right(SCREEN_WIDTH - BATTLE_WIDTH)
            ),
            controls_view
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
        if self.game_state.finished():
            self.director.replace_scene(CutScene(self.game_state))
        self.info_view.update()


class CutScene(UIScene):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        if self.game_state.finished() and self.game_state.lost():
            text = stories.fail
        elif self.game_state.level == 1 and not self.game_state.finished():
            text = stories.first
        elif self.game_state.level == 1 and self.game_state.finished():
            text = stories.second
        elif self.game_state.level == 2:
            text = stories.third
        elif self.game_state.level == 3:
            text = stories.win
        else:
            assert False, "Should never get here"

        prompt = WindowView(
            "",
            subviews=[
                LabelView(
                    utils.translate_text(text),
                    layout_options=LayoutOptions().with_updates(top=1, height=9, bottom=None)
                ),
                ButtonView(
                    "OK",
                    callback=self.callback,
                    layout_options=LayoutOptions.row_bottom(1).with_updates(right=5)
                )
            ],
            layout_options=LayoutOptions().with_updates(left=42, right=42, top=18, bottom=18)
        )
        super().__init__(views=[prompt], *args, **kwargs)

    def callback(self):
        if self.game_state.lost() or self.game_state.level == 3:
            self.director.quit()
        elif not self.game_state.finished():
            self.director.replace_scene(GameScene(self.game_state))
        else:
            self.game_state.advance_to_next_level()
            self.director.replace_scene(GameScene(self.game_state))

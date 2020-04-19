from clubsandwich.ui import LabelView, LayoutOptions, View

import utils
from logic.game_state import FPS


class InfoView(View):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        name_view = LabelView(
            utils.translate_text("Level:\n{}".format(game_state.level_name())),
            align_horz="left",
            layout_options=LayoutOptions(top=0, height=6, bottom=None)
        )
        self.time_view = LabelView(
            "",
            align_horz="left",
            layout_options=LayoutOptions(top=10, height=6, bottom=None)
        )
        self.aliens_landed = LabelView(
            "",
            align_horz="left",
            layout_options=LayoutOptions(top=20, height=6, bottom=None)
        )
        threshold_view = LabelView(
            utils.translate_text("Threshold:\n{}".format(self.game_state.escaped_enemies_limit)),
            align_horz="left",
            layout_options=LayoutOptions(top=30, height=6, bottom=None)
        )
        self.score_view = LabelView(
            "",
            align_horz="left",
            layout_options=LayoutOptions(top=40, height=6, bottom=None)
        )
        subviews = [
            name_view,
            self.time_view,
            self.aliens_landed,
            threshold_view,
            self.score_view
        ]
        super().__init__(subviews=subviews, clear=True, *args, **kwargs)

    def update(self):
        self.time_view.text = utils.translate_text("Time left:\n{}s".format(int(self.game_state.frames_left / FPS)))
        self.aliens_landed.text = utils.translate_text("Aliens landed:\n{}".format(self.game_state.escaped_enemies))
        escaped_ratio_to_limit = self.game_state.escaped_enemies / self.game_state.escaped_enemies_limit
        self.aliens_landed.color_fg = "green" if escaped_ratio_to_limit <= 0.2 else \
            "yellow" if escaped_ratio_to_limit <= 0.6 else "red"
        self.score_view.text = utils.translate_text("Score:\n{}".format(self.game_state.score))

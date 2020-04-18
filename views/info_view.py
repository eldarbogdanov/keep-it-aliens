from clubsandwich.ui import LabelView, LayoutOptions, View

import utils


class InfoView(View):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        name_view = LabelView(
            utils.translate_text("Level:\n{}".format(game_state.level_name)),
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
        subviews = [
            name_view,
            self.time_view,
            self.aliens_landed
        ]
        super().__init__(subviews=subviews, *args, **kwargs)

    def update(self):
        self.time_view.text = utils.translate_text("Time left:\n{}s".format(int(self.game_state.frames_left / 80)))
        self.aliens_landed.text = utils.translate_text("Aliens landed:\n{}".format(self.game_state.escaped_enemies))
        escaped_ratio_to_limit = self.game_state.escaped_enemies / self.game_state.escaped_enemies_limit
        self.aliens_landed.color_fg = "green" if escaped_ratio_to_limit <= 0.5 else \
            "yellow" if escaped_ratio_to_limit <= 0.8 else "red" if escaped_ratio_to_limit <= 1 else "#800000"

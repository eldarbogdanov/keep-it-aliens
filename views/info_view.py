from clubsandwich.ui import LabelView, LayoutOptions, View

from constants import FONT_OFFSET


class InfoView(View):
    def __init__(self, game_state, *args, **kwargs):
        self.game_state = game_state
        name_view = LabelView(
            self.translate_text("Level:") + "\n" + self.translate_text(game_state.level_name),
            align_horz="left",
            layout_options=LayoutOptions(top=1, height=6, bottom=None)
        )
        self.time_view = LabelView(
            "",
            align_horz="left",
            layout_options=LayoutOptions(top=10, height=6, bottom=None)
        )
        self.aliens_landed = LabelView(
            "",
            align_horz="left",
            layout_options=LayoutOptions(top=19, height=6, bottom=None)
        )
        subviews = [
            name_view,
            self.time_view,
            self.aliens_landed
        ]
        super().__init__(subviews=subviews, *args, **kwargs)

    def update(self):
        self.time_view.text = self.translate_text("Time left:") + "\n" + \
                              self.translate_text("{}s".format(int(self.game_state.frames_left / 80)))
        self.aliens_landed.text = self.translate_text("Aliens landed:") + "\n" + self.translate_text(str(self.game_state.escaped_enemies))
        escaped_ratio_to_limit = self.game_state.escaped_enemies / self.game_state.escaped_enemies_limit
        self.aliens_landed.color_fg = "green" if escaped_ratio_to_limit <= 0.5 else \
            "yellow" if escaped_ratio_to_limit <= 0.8 else "red" if escaped_ratio_to_limit <= 1 else "#800000"

    @staticmethod
    def translate_text(s):
        return "".join([chr(ord(c) + FONT_OFFSET) for c in s])

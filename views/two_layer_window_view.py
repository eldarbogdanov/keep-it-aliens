from clubsandwich.ui import WindowView, Point, Rect, Size

from utils import BACKGROUND_OFFSET


class TwoLayerWindowView(WindowView):
    def __init__(self, title, subviews, *args, **kwargs):
        super().__init__(title, subviews=subviews, *args, **kwargs)

    def draw(self, ctx):
        ctx.layer(1)
        ctx.clear_area(Rect(origin=Point(-100, -100), size=Size(300, 300)))
        ctx.layer(0)
        super().draw(ctx)
        ctx.print(Point(0, 0), chr(BACKGROUND_OFFSET))

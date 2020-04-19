from clubsandwich.ui import WindowView


class TwoLayerWindowView(WindowView):
    def __init__(self, title, subviews, *args, **kwargs):
        super().__init__(title, subviews=subviews, *args, **kwargs)

    def draw(self, ctx):
        ctx.layer(1)
        ctx.clear_area(self.bounds)
        ctx.layer(0)
        ctx.clear_area(self.bounds)
        super().draw(ctx)

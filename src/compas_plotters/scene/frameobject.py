from __future__ import annotations

from compas.geometry import Frame
from compas.scene import GeometryObject
from matplotlib.patches import ArrowStyle
from matplotlib.patches import FancyArrowPatch

from .plotterobject import PlotterSceneObject


class FrameObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Frame`.

    The frame is drawn as its projection onto the XY plane: a red arrow for the
    X axis and a green arrow for the Y axis, both starting at the frame origin.

    Parameters
    ----------
    size
        Length of the axis arrows, in data units.
    xcolor
        Color of the X-axis arrow.
    ycolor
        Color of the Y-axis arrow.
    """

    def __init__(
        self,
        size: float = 1.0,
        xcolor: tuple[float, float, float] = (1.0, 0.0, 0.0),
        ycolor: tuple[float, float, float] = (0.0, 1.0, 0.0),
        **kwargs,
    ) -> None:
        super().__init__(zorder=3000, **kwargs)
        self.size = size
        self.xcolor = xcolor
        self.ycolor = ycolor

    @property
    def frame(self) -> Frame:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        origin = self.frame.point
        ex = origin + self.frame.xaxis.scaled(self.size)
        ey = origin + self.frame.yaxis.scaled(self.size)
        return [list(origin[:2]), list(ex[:2]), list(ey[:2])]

    def _arrow(self, end, color) -> FancyArrowPatch:
        style = ArrowStyle("Simple, head_length=0.1, head_width=0.1, tail_width=0.02")
        return FancyArrowPatch(
            self.frame.point[:2],
            end[:2],
            arrowstyle=style,
            edgecolor=color,
            facecolor=color,
            zorder=self.zorder,
            mutation_scale=100,
        )

    def draw(self) -> list:
        origin = self.frame.point
        ex = origin + self.frame.xaxis.scaled(self.size)
        ey = origin + self.frame.yaxis.scaled(self.size)
        self._mpl_objects = [
            self.axes.add_patch(self._arrow(ex, self.xcolor)),
            self.axes.add_patch(self._arrow(ey, self.ycolor)),
        ]
        return self._mpl_objects

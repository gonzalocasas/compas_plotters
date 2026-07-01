from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Polyline
from compas.scene import GeometryObject
from matplotlib.lines import Line2D

from .plotterobject import PlotterSceneObject
from .plotterobject import to_color
from .plotterobject import to_rgb


class PolylineObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Polyline`.

    Parameters
    ----------
    draw_points
        If True, also draw the points of the polyline.
    linewidth
        Width of the polyline.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    color
        Color of the polyline.
    """

    def __init__(
        self,
        draw_points: bool = True,
        linewidth: float = 1.0,
        linestyle: str = "solid",
        color: Color | Sequence[float] = (0.0, 0.0, 0.0),
        **kwargs,
    ) -> None:
        super().__init__(zorder=1000, **kwargs)
        self.draw_points = draw_points
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = to_color(color)
        self._point_objects: list = []

    @property
    def polyline(self) -> Polyline:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        return [list(point[:2]) for point in self.polyline.points]

    def draw(self) -> None:
        x, y, _ = zip(*self.polyline.points)
        line2d = Line2D(
            x,
            y,
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            color=to_rgb(self.color),
            zorder=self.zorder,
        )
        self._mpl_objects = [self.axes.add_line(line2d)]
        if self.draw_points:
            self._point_objects = [self.plotter.add(point) for point in self.polyline.points]

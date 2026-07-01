from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Line
from compas.geometry import intersection_line_box_xy
from compas.scene import GeometryObject
from matplotlib.lines import Line2D

from .plotterobject import PlotterSceneObject
from .plotterobject import to_color
from .plotterobject import to_rgb


class LineObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Line`.

    By default the line is treated as infinite and clipped to the current view
    box. Set `draw_as_segment` to draw only the segment between start and end.

    Parameters
    ----------
    draw_points
        If True, also draw the start and end points of the line.
    draw_as_segment
        If True, draw only the segment between start and end instead of the
        infinite line clipped to the view box.
    linewidth
        Width of the line.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    color
        Color of the line.
    """

    def __init__(
        self,
        draw_points: bool = False,
        draw_as_segment: bool = False,
        linewidth: float = 1.0,
        linestyle: str = "solid",
        color: Color | Sequence[float] = (0.0, 0.0, 0.0),
        **kwargs,
    ) -> None:
        super().__init__(zorder=1000, **kwargs)
        self.draw_points = draw_points
        self.draw_as_segment = draw_as_segment
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = to_color(color)
        self._point_objects: list = []

    @property
    def line(self) -> Line:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        return [list(self.line.start[:2]), list(self.line.end[:2])]

    def clip(self) -> list | None:
        """Compute the intersection of the (infinite) line with the current view box.

        Returns
        -------
        The two clipping points, or None if the line does not cross the view box.
        """
        xlim, ylim = self.plotter.viewbox  # type: ignore[misc]
        xmin, xmax = xlim
        ymin, ymax = ylim
        box = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
        return intersection_line_box_xy(self.line, box)

    def draw(self) -> None:
        color = to_rgb(self.color)
        if self.draw_as_segment:
            x0, y0 = self.line.start[:2]
            x1, y1 = self.line.end[:2]
        else:
            points = self.clip()
            if not points:
                return
            (x0, y0), (x1, y1) = points[0][:2], points[1][:2]

        line2d = Line2D(
            [x0, x1],
            [y0, y1],
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            color=color,
            zorder=self.zorder,
        )
        self._mpl_objects = [self.axes.add_line(line2d)]
        if self.draw_points:
            self._point_objects = [
                self.plotter.add(self.line.start, edgecolor=color),
                self.plotter.add(self.line.end, edgecolor=color),
            ]

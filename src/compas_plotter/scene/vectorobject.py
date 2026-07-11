from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Point
from compas.geometry import Vector
from compas.scene import GeometryObject
from matplotlib.patches import ArrowStyle
from matplotlib.patches import FancyArrowPatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_color
from .plotterobject import to_rgb


class VectorObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Vector`.

    The vector is drawn as an arrow, by default starting at the world origin.

    Parameters
    ----------
    point
        The base point of the vector. Defaults to the world origin.
    draw_point
        If True, also draw the base point of the vector.
    color
        Color of the arrow.
    """

    def __init__(
        self,
        point: Point | None = None,
        draw_point: bool = False,
        color: Color | Sequence[float] = (0.0, 0.0, 0.0),
        **kwargs,
    ) -> None:
        super().__init__(zorder=3000, **kwargs)
        self.point = point or Point(0.0, 0.0, 0.0)
        self.draw_point = draw_point
        self.color = to_color(color)
        self._point_object = None

    @property
    def vector(self) -> Vector:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        return [list(self.point[:2]), list((self.point + self.vector)[:2])]

    def draw(self) -> list:
        color = to_rgb(self.color)
        style = ArrowStyle("Simple, head_length=0.1, head_width=0.1, tail_width=0.02")
        arrow = FancyArrowPatch(
            self.point[:2],
            (self.point + self.vector)[:2],
            arrowstyle=style,
            edgecolor=color,
            facecolor=color,
            zorder=self.zorder,
            mutation_scale=100,
        )
        self._mpl_objects = [self.axes.add_patch(arrow)]
        if self.draw_point:
            self._point_object = self.plotter.add(self.point, edgecolor=color)
        return self._mpl_objects

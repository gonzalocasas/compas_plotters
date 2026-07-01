from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Polygon
from compas.scene import GeometryObject
from matplotlib.patches import Polygon as PolygonPatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class PolygonObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Polygon`.

    Parameters
    ----------
    linewidth
        Width of the polygon boundary.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    facecolor
        Color of the interior of the polygon.
    edgecolor
        Color of the boundary of the polygon.
    fill
        If True, fill the interior of the polygon.
    alpha
        Transparency of the polygon, between 0 and 1.
    """

    def __init__(
        self,
        linewidth: float = 1.0,
        linestyle: str = "solid",
        facecolor: Color | Sequence[float] = (1.0, 1.0, 1.0),
        edgecolor: Color | Sequence[float] = (0.0, 0.0, 0.0),
        fill: bool = True,
        alpha: float = 1.0,
        **kwargs,
    ) -> None:
        super().__init__(zorder=1000, **kwargs)
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def polygon(self) -> Polygon:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        return [list(point[:2]) for point in self.polygon.points]

    def draw(self) -> None:
        polygon = PolygonPatch(
            self.viewdata(),
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            facecolor=to_rgb(self.facecolor),
            edgecolor=to_rgb(self.edgecolor),
            fill=self.fill,
            alpha=self.alpha,
            zorder=self.zorder,
        )
        self._mpl_objects = [self.axes.add_patch(polygon)]

from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Box
from compas.scene import GeometryObject
from matplotlib.patches import Polygon as PolygonPatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class BoxObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Box`.

    The box is drawn as its projection onto the XY plane: each of the six faces
    is projected to a semi-transparent polygon and the twelve edges are drawn on
    top, so the box reads as a solid regardless of its orientation.

    Parameters
    ----------
    linewidth
        Width of the edges.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    facecolor
        Color of the faces.
    edgecolor
        Color of the edges.
    fill
        If True, fill the faces.
    alpha
        Transparency of the faces, between 0 and 1.
    """

    def __init__(
        self,
        linewidth: float = 1.0,
        linestyle: str = "solid",
        facecolor: Color | Sequence[float] = (0.9, 0.9, 1.0),
        edgecolor: Color | Sequence[float] = (0.0, 0.0, 0.0),
        fill: bool = True,
        alpha: float = 0.3,
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
    def box(self) -> Box:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        return [list(point[:2]) for point in self.box.points]

    def draw(self) -> list:
        points = self.box.points
        # Bake the transparency into the face color only, so the edges stay solid
        # even where projected faces overlap.
        facecolor = (*to_rgb(self.facecolor), self.alpha) if self.fill else "none"
        self._mpl_objects = []
        for face in self.box.faces:
            polygon = PolygonPatch(
                [list(points[index][:2]) for index in face],
                linewidth=self.linewidth,
                linestyle=self.linestyle,
                facecolor=facecolor,
                edgecolor=to_rgb(self.edgecolor),
                fill=self.fill,
                zorder=self.zorder,
            )
            self._mpl_objects.append(self.axes.add_patch(polygon))
        return self._mpl_objects

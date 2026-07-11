from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Circle
from compas.scene import GeometryObject
from matplotlib.patches import Circle as CirclePatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class CircleObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Circle`.

    The circle is drawn as its projection onto the XY plane (center and radius);
    any out-of-plane orientation of the circle frame is ignored.

    Parameters
    ----------
    linewidth
        Width of the circle boundary.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    facecolor
        Color of the interior of the circle.
    edgecolor
        Color of the boundary of the circle.
    fill
        If True, fill the interior of the circle.
    alpha
        Transparency of the circle, between 0 and 1.
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
    def circle(self) -> Circle:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        cx, cy = self.circle.center[:2]
        r = self.circle.radius
        return [[cx - r, cy], [cx + r, cy], [cx, cy - r], [cx, cy + r]]

    def draw(self) -> list:
        circle = CirclePatch(
            self.circle.center[:2],
            radius=self.circle.radius,
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            facecolor=to_rgb(self.facecolor),
            edgecolor=to_rgb(self.edgecolor),
            fill=self.fill,
            alpha=self.alpha,
            zorder=self.zorder,
        )
        self._mpl_objects = [self.axes.add_artist(circle)]
        return self._mpl_objects

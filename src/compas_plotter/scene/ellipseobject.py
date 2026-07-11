from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Ellipse
from compas.scene import GeometryObject
from matplotlib.patches import Ellipse as EllipsePatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class EllipseObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Ellipse`.

    The ellipse is drawn as its projection onto the XY plane (center, major and
    minor axes); any out-of-plane orientation of the ellipse frame is ignored.

    Parameters
    ----------
    linewidth
        Width of the ellipse boundary.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    facecolor
        Color of the interior of the ellipse.
    edgecolor
        Color of the boundary of the ellipse.
    fill
        If True, fill the interior of the ellipse.
    alpha
        Transparency of the ellipse, between 0 and 1.
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
    def ellipse(self) -> Ellipse:
        return self.geometry  # type: ignore[return-value]

    def viewdata(self) -> list[list[float]]:
        cx, cy = self.ellipse.center[:2]
        a = self.ellipse.major
        b = self.ellipse.minor
        return [[cx - a, cy], [cx + a, cy], [cx, cy - b], [cx, cy + b]]

    def draw(self) -> list:
        ellipse = EllipsePatch(
            self.ellipse.center[:2],
            width=2 * self.ellipse.major,
            height=2 * self.ellipse.minor,
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            facecolor=to_rgb(self.facecolor),
            edgecolor=to_rgb(self.edgecolor),
            fill=self.fill,
            alpha=self.alpha,
            zorder=self.zorder,
        )
        self._mpl_objects = [self.axes.add_artist(ellipse)]
        return self._mpl_objects

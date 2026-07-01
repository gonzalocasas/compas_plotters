from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Point
from compas.scene import GeometryObject
from matplotlib.patches import Circle as CirclePatch
from matplotlib.transforms import ScaledTranslation

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class PointObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Point`.

    The point is drawn as a disc with a fixed on-screen size (in points), so it
    keeps a constant size regardless of the zoom level.

    Parameters
    ----------
    size
        The size of the point marker, in points.
    facecolor
        Color of the interior of the marker.
    edgecolor
        Color of the boundary of the marker.
    """

    def __init__(
        self,
        size: float = 5,
        facecolor: Color | Sequence[float] = (1.0, 1.0, 1.0),
        edgecolor: Color | Sequence[float] = (0.0, 0.0, 0.0),
        **kwargs,
    ) -> None:
        super().__init__(zorder=9000, **kwargs)
        self.size = size
        self.facecolor = facecolor
        self.edgecolor = edgecolor

    @property
    def point(self) -> Point:
        return self.geometry  # type: ignore[return-value]

    @property
    def _transform(self):
        # Place a fixed-size (dpi-scaled) marker at the data-space point.
        fig_scale = self.plotter.figure.dpi_scale_trans
        translation = ScaledTranslation(self.point[0], self.point[1], self.axes.transData)
        return fig_scale + translation

    def viewdata(self) -> list[list[float]]:
        return [list(self.point[:2])]

    def draw(self) -> None:
        circle = CirclePatch(
            (0, 0),
            radius=self.size / self.plotter.dpi,
            facecolor=to_rgb(self.facecolor),
            edgecolor=to_rgb(self.edgecolor),
            transform=self._transform,
            zorder=self.zorder,
        )
        self._mpl_objects = [self.axes.add_artist(circle)]

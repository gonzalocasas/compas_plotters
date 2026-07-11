from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Sequence

from compas.colors import Color
from compas.scene import SceneObject

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from compas_plotter.plotter import Plotter

RGBColor = tuple[float, float, float]


def to_rgb(color: Color | Sequence[float] | None) -> RGBColor | None:
    """Convert a COMPAS color or rgb sequence to a plain ``(r, g, b)`` tuple.

    Parameters
    ----------
    color
        A :class:`compas.colors.Color`, an rgb(a) sequence in the range 0-1, or None.

    Returns
    -------
    The rgb tuple, or None if `color` is None.
    """
    if color is None:
        return None
    if isinstance(color, Color):
        return color.rgb
    return tuple(color[:3])  # type: ignore[return-value]


def to_color(color: Color | Sequence[float] | None) -> Color | None:
    """Build a :class:`compas.colors.Color` from a color or rgb sequence.

    Unlike :meth:`compas.colors.Color.coerce`, this accepts rgb tuples that mix
    ints and floats (e.g. ``(0.5, 0, 0.5)``), which is convenient for assigning
    to the coercing ``color`` descriptors of scene objects.

    Parameters
    ----------
    color
        A :class:`compas.colors.Color`, an rgb sequence in the range 0-1, or None.

    Returns
    -------
    The color, or None if `color` is None.
    """
    if color is None:
        return None
    if isinstance(color, Color):
        return color
    return Color(*[float(c) for c in color[:3]])


class PlotterSceneObject(SceneObject):
    """Base class for all scene objects drawn by a :class:`compas_plotter.Plotter`.

    This is the COMPAS 2.x replacement for the 1.x ``PlotterArtist``. It stores a
    back-reference to the owning plotter so concrete objects can draw onto its
    matplotlib axes, and provides shared bookkeeping for the matplotlib artists
    created during drawing.

    Parameters
    ----------
    plotter
        The plotter that owns this scene object. Injected by :meth:`Plotter.add`.
    zorder
        The stacking order of this object on the canvas.
    """

    def __init__(self, plotter: Plotter | None = None, zorder: int = 1000, **kwargs) -> None:
        super().__init__(**kwargs)
        self._plotter = plotter
        self.zorder = zorder
        self._mpl_objects: list = []

    @property
    def plotter(self) -> Plotter:
        return self._plotter  # type: ignore[return-value]

    @plotter.setter
    def plotter(self, plotter: Plotter) -> None:
        self._plotter = plotter

    @property
    def axes(self) -> Axes:
        """The matplotlib axes of the owning plotter."""
        return self.plotter.axes

    def viewdata(self) -> list[list[float]]:
        """Return the 2D points bounding this object, used by :meth:`Plotter.zoom_extents`.

        Returns
        -------
        A list of ``[x, y]`` points.
        """
        return []

    def clear(self) -> None:
        """Remove all matplotlib artists previously created by this scene object."""
        for obj in self._mpl_objects:
            try:
                obj.remove()
            except (ValueError, AttributeError, NotImplementedError):
                pass
        self._mpl_objects = []

    def draw(self) -> list:
        """Draw the object on the plotter canvas. Implemented by subclasses.

        Returns
        -------
        The matplotlib artists created for this object (also stored on
        ``self._mpl_objects``), matching the :class:`compas.scene.SceneObject`
        contract that ``draw`` returns the created visualisation handles.
        """
        raise NotImplementedError

    def redraw(self) -> None:
        """Redraw the object, reflecting any changes to its geometry or settings.

        The default implementation clears the existing matplotlib artists and
        draws again. Subclasses may override this to update artists in place.
        """
        self.clear()
        self.draw()

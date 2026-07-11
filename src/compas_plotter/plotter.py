from __future__ import annotations

import os
import tempfile
from typing import TYPE_CHECKING
from typing import Callable
from typing import Iterable

import matplotlib.pyplot as plt
from compas.geometry import allclose

from compas_plotter.scene.plotterobject import PlotterSceneObject
from compas_plotter.scene.plotterscene import PlotterScene

if TYPE_CHECKING:
    from compas.data import Data
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

Viewbox = tuple[tuple[float, float], tuple[float, float]]


class Plotter:
    """Plotter for the 2D visualisation of COMPAS geometry and data structures.

    The plotter wraps a matplotlib figure and axes. COMPAS objects added to the
    plotter are dispatched through the :mod:`compas.scene` system to their
    registered ``"Plotter"`` scene object, which draws them with matplotlib.

    Parameters
    ----------
    view
        The ``((xmin, xmax), (ymin, ymax))`` area zoomed into view.
    figsize
        Size of the figure in inches.
    dpi
        Resolution of the figure in dots per inch.
    bgcolor
        Background color of the figure canvas, as a matplotlib color.
    show_axes
        If True, show the matplotlib axes.
    zstack
        If ``"natural"``, objects are stacked in the order they are added.
        If ``"zorder"``, objects are stacked by their ``zorder``.

    Attributes
    ----------
    fontsize : int
        Default font size used for labels.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas_plotter import Plotter
    >>> plotter = Plotter()
    >>> obj = plotter.add(Point(0, 0, 0))
    >>> plotter.zoom_extents()
    """

    fontsize: int = 12

    def __init__(
        self,
        view: Viewbox = ((-8.0, 16.0), (-5.0, 10.0)),
        figsize: tuple[float, float] = (8.0, 5.0),
        dpi: float = 100,
        bgcolor: str = "#ffffff",
        show_axes: bool = False,
        zstack: str = "zorder",
    ) -> None:
        self._show_axes = show_axes
        self._viewbox: Viewbox | None = None
        self._axes: Axes | None = None
        self.scene = PlotterScene(plotter=self)
        self.viewbox = view
        self.figsize = figsize
        self.dpi = dpi
        self.bgcolor = bgcolor
        self.zstack = zstack

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def viewbox(self) -> Viewbox | None:
        return self._viewbox

    @viewbox.setter
    def viewbox(self, view: Viewbox) -> None:
        xlim, ylim = view
        self._viewbox = (tuple(xlim), tuple(ylim))  # type: ignore[assignment]

    @property
    def axes(self) -> Axes:
        """The matplotlib axes used by the plotter (created lazily)."""
        if self._axes is None:
            figure = plt.figure(facecolor=self.bgcolor, figsize=self.figsize, dpi=self.dpi)
            axes = figure.add_subplot(1, 1, 1, aspect="equal")
            if self.viewbox:
                axes.set_xlim(*self.viewbox[0])
                axes.set_ylim(*self.viewbox[1])
            axes.set_xscale("linear")
            axes.set_yscale("linear")
            axes.grid(False)
            axes.set_xticks([])
            axes.set_yticks([])
            if self._show_axes:
                axes.set_frame_on(True)
                axes.spines["top"].set_color("none")
                axes.spines["right"].set_color("none")
                axes.spines["left"].set_position("zero")
                axes.spines["bottom"].set_position("zero")
            else:
                axes.set_frame_on(False)
            axes.autoscale_view()
            plt.tight_layout()
            self._axes = axes
        return self._axes

    @property
    def figure(self) -> Figure:
        """The matplotlib figure used by the plotter."""
        return self.axes.get_figure()

    @property
    def sceneobjects(self) -> list[PlotterSceneObject]:
        """The scene objects currently included in the plot."""
        return [obj for obj in self.scene.objects if isinstance(obj, PlotterSceneObject)]

    @property
    def is_live(self) -> bool:
        """Whether the matplotlib figure has been created yet."""
        return self._axes is not None

    @property
    def title(self) -> str:
        return self.figure.canvas.manager.get_window_title()

    @title.setter
    def title(self, value: str) -> None:
        self.figure.canvas.manager.set_window_title(value)

    # =========================================================================
    # Methods
    # =========================================================================

    def pause(self, pause: float) -> None:
        """Pause plotting for the given interval.

        Parameters
        ----------
        pause
            The duration of the pause, in seconds.
        """
        if pause:
            plt.pause(pause)

    def zoom_extents(self, padding: float | None = None) -> None:
        """Zoom the view to the bounding box of all drawn objects.

        Parameters
        ----------
        padding
            Extra padding around the bounding box of all objects, in data units.
        """
        padding = padding or 0.0
        width, height = self.figsize
        fig_aspect = width / height

        data: list[list[float]] = []
        for obj in self.sceneobjects:
            data += obj.viewdata()
        if not data:
            return

        x, y = zip(*data)
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        xdiff = xmax - xmin
        ydiff = ymax - ymin

        xmin = xmin - 0.1 * xdiff - padding
        xmax = xmax + 0.1 * xdiff + padding
        ymin = ymin - 0.1 * ydiff - padding
        ymax = ymax + 0.1 * ydiff + padding

        xspan = xmax - xmin
        yspan = ymax - ymin
        # Guard against degenerate (collinear / single-point) extents.
        if xspan == 0 and yspan == 0:
            xmin, xmax = xmin - 1.0, xmax + 1.0
            ymin, ymax = ymin - 1.0, ymax + 1.0
            xspan = yspan = 2.0
        elif xspan == 0:
            xmin, xmax = xmin - 0.5 * yspan, xmax + 0.5 * yspan
            xspan = xmax - xmin
        elif yspan == 0:
            ymin, ymax = ymin - 0.5 * xspan, ymax + 0.5 * xspan
            yspan = ymax - ymin

        data_aspect = xspan / yspan
        if data_aspect < fig_aspect:
            scale = fig_aspect / data_aspect
            xpad = (xspan * (scale - 1.0)) / 2.0
            xmin -= xpad
            xmax += xpad
        else:
            scale = data_aspect / fig_aspect
            ypad = (yspan * (scale - 1.0)) / 2.0
            ymin -= ypad
            ymax += ypad

        assert allclose([fig_aspect], [(xmax - xmin) / (ymax - ymin)])

        self.viewbox = ((xmin, xmax), (ymin, ymax))
        self.axes.set_xlim(xmin, xmax)
        self.axes.set_ylim(ymin, ymax)
        self.axes.autoscale_view()

    def add(self, item: Data, **kwargs) -> PlotterSceneObject:
        """Add a COMPAS object to the plot.

        Parameters
        ----------
        item
            A COMPAS geometry object or data structure.
        **kwargs
            Visualisation options forwarded to the corresponding scene object.

        Returns
        -------
        The scene object created for the item.
        """
        return self.scene.add(item, **kwargs)  # type: ignore[return-value]

    def add_from_list(self, items: Iterable[Data], **kwargs) -> list[PlotterSceneObject]:
        """Add multiple COMPAS objects, all with the same options.

        Parameters
        ----------
        items
            The COMPAS objects to add.
        **kwargs
            Visualisation options forwarded to each scene object.

        Returns
        -------
        The scene objects created for the items.
        """
        return [self.add(item, **kwargs) for item in items]

    def find(self, item: Data) -> PlotterSceneObject | None:
        """Find the scene object associated with a given COMPAS object.

        Parameters
        ----------
        item
            The COMPAS object to look for.

        Returns
        -------
        The matching scene object, or None if the item is not in the plot.
        """
        for obj in self.sceneobjects:
            if item is obj.item:
                return obj
        return None

    def register_listener(self, listener: Callable) -> None:
        """Register a listener for matplotlib pick events.

        Parameters
        ----------
        listener
            The handler called on every ``pick_event``.
        """
        self.figure.canvas.mpl_connect("pick_event", listener)

    def draw(self, pause: float | None = None) -> None:
        """Draw all objects included in the plot.

        Parameters
        ----------
        pause
            If provided, pause for this many seconds after drawing.
        """
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def redraw(self, pause: float | None = None) -> None:
        """Redraw all objects and refresh the canvas.

        Parameters
        ----------
        pause
            If provided, pause for this many seconds after redrawing.
        """
        for obj in self.sceneobjects:
            obj.redraw()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def show(self) -> None:
        """Draw all objects and display the plot in an interactive window."""
        self.draw()
        plt.show()

    def save(self, filepath: str, **kwargs) -> None:
        """Save the plot to an image file.

        Parameters
        ----------
        filepath
            Full path of the output file.
        **kwargs
            Additional keyword arguments passed to ``matplotlib.pyplot.savefig``.
        """
        self.figure.savefig(filepath, **kwargs)

    def on(
        self,
        interval: float | None = None,
        frames: int | None = None,
        record: bool = False,
        recording: str | None = None,
        dpi: int = 150,
    ) -> Callable:
        """Decorate a per-frame callback to create a dynamic (animated) plot.

        The decorated function is called once per frame with the frame index as
        its only argument, and the canvas is redrawn after each call.

        Parameters
        ----------
        interval
            Time between frames, in seconds.
        frames
            Number of frames to render.
        record
            If True, save the animation as a GIF to `recording`.
        recording
            Output path for the GIF (required when `record` is True).
        dpi
            Resolution of the recorded frames.

        Returns
        -------
        The decorator to apply to the per-frame callback.
        """
        if record and not recording:
            raise ValueError("Please provide a path for the recording.")
        if frames is None:
            raise ValueError("Please provide the number of frames.")

        def outer(func: Callable) -> None:
            if record:
                from PIL import Image

                with tempfile.TemporaryDirectory() as dirpath:
                    paths = []
                    for f in range(frames):
                        func(f)
                        self.redraw(pause=interval)
                        filepath = os.path.join(dirpath, f"frame-{f}.png")
                        paths.append(filepath)
                        self.save(filepath, dpi=dpi)
                    images = [Image.open(path) for path in paths]
                    images[0].save(
                        recording,
                        save_all=True,
                        append_images=images[1:],
                        optimize=False,
                        duration=(interval or 0.0) * 1000,
                        loop=0,
                    )
            else:
                for f in range(frames):
                    func(f)
                    self.redraw(pause=interval)

        return outer

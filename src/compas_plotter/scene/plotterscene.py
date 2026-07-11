from __future__ import annotations

from typing import TYPE_CHECKING

from compas.scene import Scene
from compas.scene import SceneObject

from .plotterobject import PlotterSceneObject

if TYPE_CHECKING:
    from compas.data import Data

    from compas_plotter.plotter import Plotter


class PlotterScene(Scene):
    """A :class:`compas.scene.Scene` bound to the ``"Plotter"`` visualisation context.

    This is the container behind a :class:`compas_plotter.Plotter`, mirroring the
    way ``compas_viewer`` wraps :class:`compas.scene.Scene` in a ``ViewerScene``.
    It stores a back-reference to the owning plotter and injects it into every
    scene object it creates, so the objects can draw onto the plotter axes.

    Parameters
    ----------
    plotter
        The plotter that owns this scene.
    name
        The name of the scene.
    context
        The visualisation context. Fixed to ``"Plotter"``; overriding it would
        prevent the plotter scene objects from being resolved.
    """

    def __init__(self, plotter: Plotter | None = None, name: str = "PlotterScene", context: str = "Plotter") -> None:
        super().__init__(name=name, context=context)
        self.plotter = plotter

    def add(self, item: Data | SceneObject, parent=None, **kwargs) -> SceneObject:
        """Add an item to the scene and draw it on the plotter canvas.

        Extends :meth:`compas.scene.Scene.add` by injecting the owning plotter
        into the created scene object and drawing it immediately, so that adding
        an object to a live plot shows it right away.

        Parameters
        ----------
        item
            The COMPAS object (or ready-made scene object) to add.
        parent
            The parent scene object in the scene tree.
        **kwargs
            Visualisation options forwarded to the scene object.

        Returns
        -------
        The scene object created for the item.
        """
        if not isinstance(item, SceneObject) and self.plotter is not None:
            kwargs.setdefault("plotter", self.plotter)
            if getattr(self.plotter, "zstack", "zorder") == "natural":
                kwargs.setdefault("zorder", 1000 + len(self.objects) * 100)

        sceneobject = super().add(item, parent=parent, **kwargs)

        if isinstance(sceneobject, PlotterSceneObject):
            sceneobject.draw()

        return sceneobject

    def remove(self, sceneobject: SceneObject) -> None:
        """Remove a scene object, clearing its matplotlib artists first.

        Parameters
        ----------
        sceneobject
            The scene object to remove.
        """
        if isinstance(sceneobject, PlotterSceneObject):
            sceneobject.clear()
        super().remove(sceneobject)

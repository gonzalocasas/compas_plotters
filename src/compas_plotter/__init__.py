"""2D visualisation of COMPAS geometry and data structures with matplotlib.

This is the COMPAS 2.x successor of the ``compas_plotter`` package that shipped
inside COMPAS up to version 1.17. It registers a ``"Plotter"`` visualisation
context built on top of the modern :mod:`compas.scene` system, so any COMPAS
object with a registered plotter scene object can be drawn with
:meth:`compas_plotter.Plotter.add`.
"""

from .__version__ import __version__
from .plotter import Plotter

# COMPAS plugin discovery imports the modules listed here to find the
# ``@plugin``-decorated ``register_scene_objects`` factory.
__all_plugins__ = ["compas_plotter.scene"]

__all__ = ["Plotter", "__version__"]

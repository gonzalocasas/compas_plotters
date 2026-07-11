"""2D visualisation of COMPAS geometry and data structures with matplotlib.

This is the COMPAS 2.x successor of the ``compas_plotter`` package that shipped
inside COMPAS up to version 1.17. It registers a ``"Plotter"`` visualisation
context built on top of the modern :mod:`compas.scene` system, so any COMPAS
object with a registered plotter scene object can be drawn with
:meth:`compas_plotter.Plotter.add`.
"""

from .__version__ import __version__
from .plotter import Plotter

# Importing the scene subpackage triggers registration of the Plotter scene
# objects. When this package is pip-installed, COMPAS would also discover the
# @plugin-decorated factory through the entry point; importing here guarantees
# registration works in editable / non-installed setups as well.
from . import scene  # noqa: E402,F401

__all__ = ["Plotter", "__version__"]

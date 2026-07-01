"""Plotter scene objects and their registration.

This subpackage is the ``"Plotter"`` visualisation-context backend, mirroring the
structure of ``compas_rhino.scene`` and ``compas_blender.scene``: it provides a
scene object per supported COMPAS type and registers each one under the
``"Plotter"`` context.
"""

from __future__ import annotations

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Vector
from compas.plugins import plugin
from compas.scene import register

from .circleobject import CircleObject
from .ellipseobject import EllipseObject
from .frameobject import FrameObject
from .graphobject import GraphObject
from .lineobject import LineObject
from .meshobject import MeshObject
from .plotterobject import PlotterSceneObject
from .pointobject import PointObject
from .polygonobject import PolygonObject
from .polylineobject import PolylineObject
from .vectorobject import VectorObject


@plugin(category="factories", requires=["matplotlib"])
def register_scene_objects():
    """Register all Plotter scene objects under the ``"Plotter"`` context."""
    register(Point, PointObject, context="Plotter")
    register(Vector, VectorObject, context="Plotter")
    register(Line, LineObject, context="Plotter")
    register(Polyline, PolylineObject, context="Plotter")
    register(Polygon, PolygonObject, context="Plotter")
    register(Circle, CircleObject, context="Plotter")
    register(Ellipse, EllipseObject, context="Plotter")
    register(Frame, FrameObject, context="Plotter")
    register(Mesh, MeshObject, context="Plotter")
    register(Graph, GraphObject, context="Plotter")


# Eager registration so that the Plotter works in editable / non-installed setups
# (where the entry-point-based plugin discovery does not run).
register_scene_objects()


__all__ = [
    "PlotterSceneObject",
    "PointObject",
    "VectorObject",
    "LineObject",
    "PolylineObject",
    "PolygonObject",
    "CircleObject",
    "EllipseObject",
    "FrameObject",
    "MeshObject",
    "GraphObject",
]

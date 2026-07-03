"""Plotter scene objects and their registration.

This subpackage is the ``"Plotter"`` visualisation-context backend, mirroring the
structure of ``compas_rhino.scene`` and ``compas_blender.scene``: it provides a
scene object per supported COMPAS type and registers each one under the
``"Plotter"`` context.
"""

from __future__ import annotations

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.geometry import Box
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

from .boxobject import BoxObject
from .circleobject import CircleObject
from .ellipseobject import EllipseObject
from .frameobject import FrameObject
from .graphobject import GraphObject
from .lineobject import LineObject
from .meshobject import MeshObject
from .plotterobject import PlotterSceneObject
from .plotterscene import PlotterScene
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
    register(Box, BoxObject, context="Plotter")
    register(Mesh, MeshObject, context="Plotter")
    register(Graph, GraphObject, context="Plotter")

    # Roadmap: 3D shapes, Breps and surfaces are drawn via XY projection once
    # their scene objects are implemented. Registration is guarded so the package
    # keeps working until then, and lights up automatically when the objects (and
    # any optional dependencies, e.g. compas_occ for Breps) become available.
    try:
        from compas.geometry import Capsule
        from compas.geometry import Cone
        from compas.geometry import Cylinder
        from compas.geometry import Polyhedron
        from compas.geometry import Sphere
        from compas.geometry import Torus

        from .shapeobject import ShapeObject

        for shape_cls in (Sphere, Cylinder, Cone, Capsule, Torus, Polyhedron):
            register(shape_cls, ShapeObject, context="Plotter")
    except ImportError:
        pass


# Eager registration so that the Plotter works in editable / non-installed setups
# (where the entry-point-based plugin discovery does not run).
register_scene_objects()


__all__ = [
    "PlotterScene",
    "PlotterSceneObject",
    "PointObject",
    "VectorObject",
    "LineObject",
    "PolylineObject",
    "PolygonObject",
    "CircleObject",
    "EllipseObject",
    "FrameObject",
    "BoxObject",
    "MeshObject",
    "GraphObject",
]

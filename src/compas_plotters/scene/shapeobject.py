from __future__ import annotations

from typing import Sequence

from compas.colors import Color
from compas.geometry import Shape
from compas.scene import GeometryObject
from matplotlib.patches import Polygon as PolygonPatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class ShapeObject(PlotterSceneObject, GeometryObject):
    """Plotter scene object for :class:`compas.geometry.Shape`.

    Handles all COMPAS solids (Sphere, Cylinder, Cone, Capsule, Torus,
    Polyhedron, ...). The shape is tessellated with
    :meth:`compas.geometry.Shape.to_vertices_and_faces` and drawn as the
    projection of that mesh onto the XY plane: each face becomes a
    semi-transparent polygon with a solid outline, so the shape reads as a solid
    wireframe regardless of its orientation.

    Parameters
    ----------
    u
        Number of faces around curved shapes (longitude). Ignored by shapes
        without a resolution, such as :class:`compas.geometry.Polyhedron`.
    v
        Number of faces along curved shapes (latitude), where applicable.
    linewidth
        Width of the edges.
    linestyle
        Matplotlib line style (``"solid"``, ``"dotted"``, ``"dashed"``, ``"dashdot"``).
    facecolor
        Color of the faces.
    edgecolor
        Color of the edges.
    fill
        If True, fill the faces.
    alpha
        Transparency of the faces, between 0 and 1.
    """

    def __init__(
        self,
        u: int = 16,
        v: int = 16,
        linewidth: float = 0.5,
        linestyle: str = "solid",
        facecolor: Color | Sequence[float] = (0.9, 0.9, 1.0),
        edgecolor: Color | Sequence[float] = (0.0, 0.0, 0.0),
        fill: bool = True,
        alpha: float = 0.2,
        **kwargs,
    ) -> None:
        super().__init__(zorder=1000, **kwargs)
        self.u = u
        self.v = v
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def shape(self) -> Shape:
        return self.geometry  # type: ignore[return-value]

    def _vertices_and_faces(self) -> tuple[list, list]:
        try:
            return self.shape.to_vertices_and_faces(u=self.u, v=self.v)
        except TypeError:
            # Shapes without a resolution (e.g. Polyhedron) take no u/v.
            return self.shape.to_vertices_and_faces()

    def viewdata(self) -> list[list[float]]:
        vertices, _ = self._vertices_and_faces()
        return [list(vertex[:2]) for vertex in vertices]

    def draw(self) -> list:
        vertices, faces = self._vertices_and_faces()
        # Bake the transparency into the face color only, so the edges stay solid
        # even where projected faces overlap.
        facecolor = (*to_rgb(self.facecolor), self.alpha) if self.fill else "none"
        self._mpl_objects = []
        for face in faces:
            polygon = PolygonPatch(
                [list(vertices[index][:2]) for index in face],
                linewidth=self.linewidth,
                linestyle=self.linestyle,
                facecolor=facecolor,
                edgecolor=to_rgb(self.edgecolor),
                fill=self.fill,
                zorder=self.zorder,
            )
            self._mpl_objects.append(self.axes.add_patch(polygon))
        return self._mpl_objects

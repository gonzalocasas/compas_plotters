from __future__ import annotations

from compas.colors import Color
from compas.geometry import centroid_points_xy
from compas.geometry import transform_points
from compas.scene import MeshObject as BaseMeshObject
from matplotlib.collections import LineCollection
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from matplotlib.patches import Polygon as PolygonPatch

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class MeshObject(PlotterSceneObject, BaseMeshObject):
    """Plotter scene object for :class:`compas.datastructures.Mesh`.

    Reuses the data layer of the COMPAS 2.x base mesh scene object (the
    ``show_vertices/edges/faces`` flags and the per-element color/size settings)
    and provides the matplotlib drawing backend, including optional labels.

    Parameters
    ----------
    vertexsize
        On-screen size of the vertex markers, in points.
    edgewidth
        Width of the edges.
    facecolor
        Color of the faces. A single color, or a dict mapping faces to colors.
    edgecolor
        Color of the edges. A single color, or a dict mapping edges to colors.
    vertexcolor
        Color of the vertices. A single color, or a dict mapping vertices to colors.
    vertextext
        A dict mapping vertices to label strings.
    edgetext
        A dict mapping edges to label strings.
    facetext
        A dict mapping faces to label strings.
    """

    def __init__(
        self,
        vertexsize: float = 5,
        edgewidth: float = 1.0,
        facecolor=(0.9, 0.9, 0.9),
        edgecolor=(0.0, 0.0, 0.0),
        vertexcolor=(1.0, 1.0, 1.0),
        vertextext: dict | None = None,
        edgetext: dict | None = None,
        facetext: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            zorder=1000,
            vertexsize=vertexsize,
            edgewidth=edgewidth,
            facecolor=facecolor,
            edgecolor=edgecolor,
            vertexcolor=vertexcolor,
            **kwargs,
        )
        self.vertextext = vertextext or {}
        self.edgetext = edgetext or {}
        self.facetext = facetext or {}

    @property
    def vertex_xyz(self) -> dict:
        """Mapping of vertices to their world coordinates."""
        vertices = list(self.mesh.vertices())
        points = [self.mesh.vertex_coordinates(vertex) for vertex in vertices]
        points = transform_points(points, self.worldtransformation)
        return dict(zip(vertices, points))

    def viewdata(self) -> list[list[float]]:
        return [xyz[:2] for xyz in self.vertex_xyz.values()]

    def draw(self) -> None:
        vertex_xyz = self.vertex_xyz
        if self.show_faces:
            self._draw_faces(vertex_xyz)
        if self.show_edges:
            self._draw_edges(vertex_xyz)
        if self.show_vertices:
            self._draw_vertices(vertex_xyz)
        self._draw_labels(vertex_xyz)

    def _draw_faces(self, vertex_xyz: dict) -> None:
        patches = []
        colors = []
        for face in self.mesh.faces():
            points = [vertex_xyz[vertex][:2] for vertex in self.mesh.face_vertices(face)]
            patches.append(PolygonPatch(points, closed=True))
            colors.append(to_rgb(self.facecolor[face]))
        collection = PatchCollection(patches, facecolor=colors, edgecolor="none", zorder=self.zorder)
        self.axes.add_collection(collection)
        self._mpl_objects.append(collection)

    def _draw_edges(self, vertex_xyz: dict) -> None:
        lines = []
        colors = []
        for u, v in self.mesh.edges():
            lines.append([vertex_xyz[u][:2], vertex_xyz[v][:2]])
            colors.append(to_rgb(self.edgecolor[(u, v)]))
        collection = LineCollection(lines, linewidths=self.edgewidth, colors=colors, zorder=self.zorder + 10)
        self.axes.add_collection(collection)
        self._mpl_objects.append(collection)

    def _draw_vertices(self, vertex_xyz: dict) -> None:
        circles = []
        radius = self.vertexsize / self.plotter.dpi
        for vertex in self.mesh.vertices():
            x, y = vertex_xyz[vertex][:2]
            circles.append(
                Circle(
                    (x, y),
                    radius=radius,
                    facecolor=to_rgb(self.vertexcolor[vertex]),
                    edgecolor=(0, 0, 0),
                    lw=0.3,
                )
            )
        collection = PatchCollection(circles, match_original=True, zorder=self.zorder + 20)
        self.axes.add_collection(collection)
        self._mpl_objects.append(collection)

    def _draw_labels(self, vertex_xyz: dict) -> None:
        for vertex, text in self.vertextext.items():
            x, y = vertex_xyz[vertex][:2]
            bgcolor = Color(*to_rgb(self.vertexcolor[vertex]))
            color = (0, 0, 0) if bgcolor.is_light else (1, 1, 1)
            self._mpl_objects.append(self._text(x, y, text, color))

        for (u, v), text in self.edgetext.items():
            x0, y0 = vertex_xyz[u][:2]
            x1, y1 = vertex_xyz[v][:2]
            self._mpl_objects.append(self._text(0.5 * (x0 + x1), 0.5 * (y0 + y1), text, (0, 0, 0), boxed=True))

        for face, text in self.facetext.items():
            x, y, _ = centroid_points_xy([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])
            self._mpl_objects.append(self._text(x, y, text, (0, 0, 0), boxed=True))

    def _text(self, x, y, text, color, boxed: bool = False):
        bbox = None
        if boxed:
            bbox = dict(boxstyle="round, pad=0.3", facecolor=(1, 1, 1), edgecolor="none", linewidth=0)
        return self.axes.text(
            x,
            y,
            f"{text}",
            fontsize=self.plotter.fontsize,
            family="monospace",
            ha="center",
            va="center",
            zorder=10000,
            color=color,
            bbox=bbox,
        )

from __future__ import annotations

from compas.colors import Color
from compas.geometry import transform_points
from compas.scene import GraphObject as BaseGraphObject
from matplotlib.collections import LineCollection
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

from .plotterobject import PlotterSceneObject
from .plotterobject import to_rgb


class GraphObject(PlotterSceneObject, BaseGraphObject):
    """Plotter scene object for :class:`compas.datastructures.Graph`.

    Reuses the data layer of the COMPAS 2.x base graph scene object (the
    ``show_nodes/edges`` flags and the per-element color/size settings, and the
    ``node_xyz`` coordinate map) and provides the matplotlib drawing backend,
    including optional labels.

    Parameters
    ----------
    nodesize
        Size of the node markers.
    edgewidth
        Width of the edges.
    nodecolor
        Color of the nodes. A single color, or a dict mapping nodes to colors.
    edgecolor
        Color of the edges. A single color, or a dict mapping edges to colors.
    sizepolicy
        If ``"absolute"``, `nodesize` is scaled by the plotter resolution, giving
        nodes a constant on-screen size (the default).
        If ``"relative"``, `nodesize` is scaled by the number of nodes.
    nodetext
        A dict mapping nodes to label strings.
    edgetext
        A dict mapping edges to label strings.
    """

    def __init__(
        self,
        nodesize: float = 5,
        edgewidth: float = 1.0,
        nodecolor=(1.0, 1.0, 1.0),
        edgecolor=(0.0, 0.0, 0.0),
        sizepolicy: str = "absolute",
        nodetext: dict | None = None,
        edgetext: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            zorder=1000,
            nodesize=nodesize,
            edgewidth=edgewidth,
            nodecolor=nodecolor,
            edgecolor=edgecolor,
            **kwargs,
        )
        self.sizepolicy = sizepolicy
        self.nodetext = nodetext or {}
        self.edgetext = edgetext or {}

    @property
    def node_xyz(self) -> dict:
        """Mapping of nodes to their view coordinates."""
        if self._node_xyz is not None:
            return self._node_xyz
        nodes = list(self.graph.nodes())
        points = self.graph.nodes_attributes("xyz", keys=nodes)
        points = transform_points(points, self.worldtransformation)
        return dict(zip(nodes, points))

    @node_xyz.setter
    def node_xyz(self, node_xyz: dict | None) -> None:
        self._node_xyz = node_xyz

    def _node_radius(self) -> float:
        factor = self.plotter.dpi if self.sizepolicy == "absolute" else max(self.graph.number_of_nodes(), 1)
        return self.nodesize / factor

    def viewdata(self) -> list[list[float]]:
        return [xyz[:2] for xyz in self.node_xyz.values()]

    def draw(self) -> list:
        node_xyz = self.node_xyz
        if self.show_edges:
            self._draw_edges(node_xyz)
        if self.show_nodes:
            self._draw_nodes(node_xyz)
        self._draw_labels(node_xyz)
        return self._mpl_objects

    def _draw_nodes(self, node_xyz: dict) -> None:
        radius = self._node_radius()
        circles = []
        for node in self.graph.nodes():
            x, y = node_xyz[node][:2]
            circles.append(
                Circle(
                    (x, y),
                    radius=radius,
                    facecolor=to_rgb(self.nodecolor[node]),
                    edgecolor=(0, 0, 0),
                    lw=0.3,
                )
            )
        collection = PatchCollection(circles, match_original=True, zorder=self.zorder + 20)
        self.axes.add_collection(collection)
        self._mpl_objects.append(collection)

    def _draw_edges(self, node_xyz: dict) -> None:
        lines = []
        colors = []
        for u, v in self.graph.edges():
            lines.append([node_xyz[u][:2], node_xyz[v][:2]])
            colors.append(to_rgb(self.edgecolor[(u, v)]))
        collection = LineCollection(lines, linewidths=self.edgewidth, colors=colors, zorder=self.zorder + 10)
        self.axes.add_collection(collection)
        self._mpl_objects.append(collection)

    def _draw_labels(self, node_xyz: dict) -> None:
        for node, text in self.nodetext.items():
            x, y = node_xyz[node][:2]
            bgcolor = Color(*to_rgb(self.nodecolor[node]))
            color = (0, 0, 0) if bgcolor.is_light else (1, 1, 1)
            self._mpl_objects.append(self._text(x, y, text, color))

        for (u, v), text in self.edgetext.items():
            x0, y0 = node_xyz[u][:2]
            x1, y1 = node_xyz[v][:2]
            self._mpl_objects.append(self._text(0.5 * (x0 + x1), 0.5 * (y0 + y1), text, (0, 0, 0), boxed=True))

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

import matplotlib

matplotlib.use("Agg")

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

from compas_plotters import Plotter
from compas_plotters.scene import CircleObject
from compas_plotters.scene import EllipseObject
from compas_plotters.scene import FrameObject
from compas_plotters.scene import GraphObject
from compas_plotters.scene import LineObject
from compas_plotters.scene import MeshObject
from compas_plotters.scene import PointObject
from compas_plotters.scene import PolygonObject
from compas_plotters.scene import PolylineObject
from compas_plotters.scene import VectorObject


def test_add_point_returns_pointobject():
    plotter = Plotter()
    obj = plotter.add(Point(0, 0, 0))
    assert isinstance(obj, PointObject)
    assert plotter.find(obj.item) is obj


def test_add_all_geometry_types():
    plotter = Plotter()
    pairs = [
        (Vector(1, 0, 0), VectorObject),
        (Line(Point(0, 0, 0), Point(1, 1, 0)), LineObject),
        (Polyline([[0, 0, 0], [1, 0, 0], [1, 1, 0]]), PolylineObject),
        (Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0]]), PolygonObject),
        (Circle(1.0), CircleObject),
        (Ellipse(2.0, 1.0), EllipseObject),
        (Frame.worldXY(), FrameObject),
    ]
    for item, expected in pairs:
        obj = plotter.add(item)
        assert isinstance(obj, expected)
    assert len(plotter.sceneobjects) >= len(pairs)


def test_add_mesh_and_graph():
    plotter = Plotter()
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 1, 2, 3]],
    )
    mobj = plotter.add(mesh, show_vertices=True, show_edges=True)
    assert isinstance(mobj, MeshObject)
    assert len(mobj.vertex_xyz) == 4

    graph = Graph()
    a = graph.add_node(x=0, y=0, z=0)
    b = graph.add_node(x=1, y=1, z=0)
    graph.add_edge(a, b)
    gobj = plotter.add(graph)
    assert isinstance(gobj, GraphObject)


def test_zoom_extents_no_objects_is_noop():
    plotter = Plotter()
    plotter.zoom_extents()  # should not raise


def test_save(tmp_path):
    plotter = Plotter(figsize=(4, 4))
    plotter.add(Point(0, 0, 0))
    plotter.add(Line(Point(0, 0, 0), Point(2, 2, 0)), draw_as_segment=True)
    plotter.zoom_extents()
    out = tmp_path / "out.png"
    plotter.save(str(out))
    assert out.exists() and out.stat().st_size > 0


def test_redraw_clears_and_redraws():
    plotter = Plotter()
    obj = plotter.add(Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0]]))
    n_before = len(obj._mpl_objects)
    obj.redraw()
    assert len(obj._mpl_objects) == n_before


def test_dynamic_on_runs_frames():
    plotter = Plotter()
    point = Point(0, 0, 0)
    plotter.add(point)
    seen = []

    @plotter.on(interval=0, frames=3)
    def frame(f):
        seen.append(f)
        point.x = f

    assert seen == [0, 1, 2]

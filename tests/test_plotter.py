import matplotlib

matplotlib.use("Agg")

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Vector

from compas_plotters import Plotter
from compas_plotters.scene import BoxObject
from compas_plotters.scene import CircleObject
from compas_plotters.scene import EllipseObject
from compas_plotters.scene import FrameObject
from compas_plotters.scene import GraphObject
from compas_plotters.scene import LineObject
from compas_plotters.scene import MeshObject
from compas_plotters.scene import PointObject
from compas_plotters.scene import PolygonObject
from compas_plotters.scene import PolylineObject
from compas_plotters.scene import ShapeObject
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


def test_add_box_returns_boxobject():
    plotter = Plotter()
    obj = plotter.add(Box(1, 2, 3))
    assert isinstance(obj, BoxObject)
    # one patch per face
    assert len(obj._mpl_objects) == 6
    assert len(obj.viewdata()) == 8


def test_add_all_shape_types():
    plotter = Plotter()
    shapes = [
        Sphere(1.0),
        Cylinder(0.5, 2.0),
        Cone(0.5, 2.0),
        Capsule(0.3, 1.5),
        Torus(1.0, 0.3),
        Polyhedron.from_platonicsolid(12),
    ]
    for shape in shapes:
        obj = plotter.add(shape)
        assert isinstance(obj, ShapeObject)
        # every tessellated face is drawn
        _, faces = obj._vertices_and_faces()
        assert len(obj._mpl_objects) == len(faces) > 0


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


def test_scene_is_a_compas_scene():
    from compas.scene import Scene

    from compas_plotters.scene import PlotterScene

    plotter = Plotter()
    assert isinstance(plotter.scene, PlotterScene)
    assert isinstance(plotter.scene, Scene)
    assert plotter.scene.context == "Plotter"


def test_scene_hierarchy_and_world_transform():
    from compas.geometry import Translation

    plotter = Plotter()
    parent = plotter.add(Point(0, 0, 0))
    child = plotter.add(Point(1, 0, 0), parent=parent)
    assert child.parent is parent
    assert len(plotter.scene.objects) == 2

    parent.transformation = Translation.from_vector([10, 0, 0])
    assert child.worldtransformation[0, 3] == 10.0


def test_scene_remove_clears_and_detaches():
    plotter = Plotter()
    obj = plotter.add(Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0]]))
    assert len(plotter.sceneobjects) == 1
    plotter.scene.remove(obj)
    assert len(plotter.sceneobjects) == 0
    assert obj._mpl_objects == []


def test_scene_draw_returns_artists():
    plotter = Plotter()
    plotter.add(Point(0, 0, 0))
    plotter.add(Line(Point(0, 0, 0), Point(2, 2, 0)), draw_as_segment=True)
    drawn = plotter.scene.draw()
    assert isinstance(drawn, list)
    assert len(drawn) == 2


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


def test_dynamic_on_updates_graph_node_xyz():
    plotter = Plotter()
    graph = Graph()
    a = graph.add_node(x=0, y=0, z=0)
    b = graph.add_node(x=1, y=0, z=0)
    graph.add_edge(a, b)
    obj = plotter.add(graph)

    @plotter.on(interval=0, frames=3)
    def frame(f):
        x = graph.node_attribute(b, "x")
        graph.node_attribute(b, "x", x + f)

    assert obj.node_xyz[b][0] == 4.0


def test_mesh_vertex_xyz_is_fresh_and_assignable():
    plotter = Plotter()
    mesh = Mesh.from_vertices_and_faces(
        {0: [0.0, 0.0, 0.0], 1: [1.0, 0.0, 0.0], 2: [1.0, 1.0, 0.0], 3: [0.0, 1.0, 0.0]},
        [[0, 1, 2, 3]],
    )
    obj = plotter.add(mesh)

    @plotter.on(interval=0, frames=3)
    def frame(f):
        y = mesh.vertex_attribute(1, "y")
        mesh.vertex_attribute(1, "y", y + f)

        z = mesh.vertex_attribute(3, "z")
        mesh.vertex_attribute(3, "z", z + f)

    assert obj.vertex_xyz[1][1] == 3.0
    assert obj.vertex_xyz[3][2] == 3.0

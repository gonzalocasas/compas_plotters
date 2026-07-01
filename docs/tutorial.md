# Tutorial

`compas_plotters` draws COMPAS objects onto a matplotlib canvas. The main entry
point is the [`Plotter`][compas_plotters.Plotter] class. You add objects to it
with [`Plotter.add`][compas_plotters.Plotter.add], and each object is dispatched
through the [`compas.scene`](https://compas.dev/compas/latest/) system to a
matplotlib-based scene object.

## A first plot

```python
from compas.geometry import Point
from compas_plotters import Plotter

plotter = Plotter()
plotter.add(Point(0, 0, 0))
plotter.add(Point(1, 0, 0))
plotter.add(Point(1, 1, 0))
plotter.zoom_extents()
plotter.show()
```

`zoom_extents` fits the view to the bounding box of everything that has been
added, while preserving the aspect ratio of the figure.

## Adding geometry

Every supported geometry type is added the same way. Keyword arguments are
forwarded to the corresponding scene object to control its appearance.

```python
from compas.geometry import Point, Vector, Line, Polyline, Polygon, Circle, Ellipse, Frame
from compas_plotters import Plotter

plotter = Plotter(figsize=(8, 5))

plotter.add(Line(Point(0, 0, 0), Point(3, 2, 0)), color=(1, 0, 0), draw_as_segment=True)
plotter.add(Polyline([[0, 0, 0], [1, 1, 0], [2, 0, 0]]), color=(0, 0, 1))
plotter.add(Polygon([[3, 0, 0], [5, 0, 0], [5, 2, 0]]), facecolor=(0.9, 0.9, 1.0))
plotter.add(Circle(1.0, frame=Frame([6, 1, 0])))
plotter.add(Ellipse(1.5, 0.8, frame=Frame([9, 1, 0])))
plotter.add(Vector(1, 1, 0), point=Point(0, -2, 0), draw_point=True)
plotter.add(Frame([6, -2, 0]), size=1.0)
plotter.add(Point(0, 0, 0))

plotter.zoom_extents()
plotter.show()
```

### Lines: segments vs. infinite lines

A `Line` in COMPAS is infinite. By default the `LineObject` clips the line to
the current view box. Pass `draw_as_segment=True` to draw only the segment
between `line.start` and `line.end`.

### Points keep a constant size

Points (and mesh vertices and graph nodes) are drawn with a fixed on-screen size
in points, so they do not grow or shrink when you zoom.

## Meshes

Meshes reuse the data layer of the COMPAS scene system, so the `show_vertices`,
`show_edges` and `show_faces` flags and the per-element colors work as expected.

```python
from compas.datastructures import Mesh
from compas_plotters import Plotter

mesh = Mesh.from_meshgrid(dx=10, nx=10)

plotter = Plotter(figsize=(8, 8))
plotter.add(
    mesh,
    show_vertices=True,
    show_edges=True,
    facecolor={face: (0.9, 0.9, 1.0) for face in mesh.faces()},
)
plotter.zoom_extents()
plotter.show()
```

Labels are drawn by passing `vertextext`, `edgetext` or `facetext` dictionaries:

```python
plotter.add(mesh, facetext={face: str(face) for face in mesh.faces()})
```

## Graphs

```python
from compas.datastructures import Graph
from compas_plotters import Plotter

graph = Graph()
a = graph.add_node(x=0, y=0, z=0)
b = graph.add_node(x=1, y=1, z=0)
c = graph.add_node(x=2, y=0, z=0)
graph.add_edge(a, b)
graph.add_edge(b, c)

plotter = Plotter()
plotter.add(graph, nodesize=10, nodetext={a: "a", b: "b", c: "c"})
plotter.zoom_extents()
plotter.show()
```

## Saving

```python
plotter.save("figure.png", dpi=300)
```

## Dynamic plots and animations

[`Plotter.on`][compas_plotters.Plotter.on] turns a plotter into an animation
loop. The decorated function is called once per frame; mutate your geometry and
the plotter redraws it. Set `record` and `recording` to also export a GIF.

```python
from compas.geometry import Point
from compas_plotters import Plotter

plotter = Plotter()
point = Point(0, 0, 0)
plotter.add(point)
plotter.zoom_extents()

@plotter.on(interval=0.1, frames=50, record=True, recording="point.gif")
def move(frame):
    point.x = 0.1 * frame

plotter.show()
```

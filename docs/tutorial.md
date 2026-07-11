# Tutorial

`compas_plotter` draws COMPAS objects onto a matplotlib canvas. The main entry
point is the [`Plotter`][compas_plotter.Plotter] class. You add objects to it
with [`Plotter.add`][compas_plotter.Plotter.add], and each object is dispatched
through the [`compas.scene`](https://compas.dev/compas/latest/) system to a
matplotlib-based scene object.

## A first plot

```python
from compas.geometry import Point
from compas_plotter import Plotter

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
from compas_plotter import Plotter

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

## 3D shapes

3D shapes are drawn as their projection onto the XY plane. A `Box`, for example,
is projected face by face, so it reads as a solid wireframe regardless of how its
frame is oriented. The same works for `Sphere`, `Cylinder`, `Cone`, `Capsule`,
`Torus` and `Polyhedron`: they are tessellated into a mesh and that mesh is
projected. Curved shapes take `u`/`v` keyword arguments to control the
tessellation resolution.

```python
from compas.geometry import Sphere, Cylinder, Cone, Torus, Polyhedron
from compas.geometry import Translation
from compas_plotter import Plotter

plotter = Plotter(figsize=(10, 3))

plotter.add(Sphere(1.0))
plotter.add(Cylinder(0.6, 2.0).transformed(Translation.from_vector([3, 0, 0])))
plotter.add(Cone(0.8, 2.0).transformed(Translation.from_vector([6, 0, 0])), u=12)
plotter.add(Torus(1.0, 0.3).transformed(Translation.from_vector([9, 0, 0])))
plotter.add(Polyhedron.from_platonicsolid(12).transformed(Translation.from_vector([12, 0, 0])))

plotter.zoom_extents()
plotter.show()
```

The `Box` below is projected the same way.

```python
from math import radians
from compas.geometry import Box, Frame
from compas_plotter import Plotter

plotter = Plotter(figsize=(8, 5))

# an axis-aligned box projects to a rectangle
plotter.add(Box(3, 2, 1))

# a rotated box keeps its 3D silhouette
frame = Frame([6, 0, 0]).rotated(radians(35), [1, 1, 1], point=[6, 0, 0])
plotter.add(Box(2, 2, 2, frame=frame), facecolor=(0.9, 0.9, 1.0), alpha=0.3)

plotter.zoom_extents()
plotter.show()
```

Pass `fill=False` for a pure wireframe, or tune `alpha` and `facecolor` to shade
the faces. Because a projection has no depth sorting, faces are not hidden behind
one another — every edge stays visible.

### Rotating box animation

A good way to confirm the projection is spinning the box and watching the
silhouette update every frame. Rotate the geometry inside a
[`Plotter.on`][compas_plotter.Plotter.on] callback (see
[Dynamic plots and animations](#dynamic-plots-and-animations)) and the plotter
reprojects and redraws it:

```python
from math import radians
from compas.geometry import Box, Frame, Rotation
from compas_plotter import Plotter

plotter = Plotter(figsize=(6, 6))

box = Box(2, 2, 2, frame=Frame([0, 0, 0]).rotated(radians(35), [1, 1, 1]))
plotter.add(box, facecolor=(0.9, 0.9, 1.0), alpha=0.3)

# keep the view fixed so the box is seen to rotate, not the camera
plotter.zoom_extents()

rotation = Rotation.from_axis_and_angle([0, 1, 0], radians(6), point=[0, 0, 0])

@plotter.on(interval=0.05, frames=60, record=True, recording="box.gif")
def spin(frame):
    box.transform(rotation)

plotter.show()
```

Each frame applies a small rotation; the six faces are re-projected onto the XY
plane, so the wireframe appears to turn in 3D. Any of the shapes above can be
animated the same way.

## Meshes

Meshes reuse the data layer of the COMPAS scene system, so the `show_vertices`,
`show_edges` and `show_faces` flags and the per-element colors work as expected.

```python
from compas.datastructures import Mesh
from compas_plotter import Plotter

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
from compas_plotter import Plotter

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

## Scenes and hierarchy

Every `Plotter` owns a [`PlotterScene`][compas_plotter.scene.PlotterScene], a
subclass of [`compas.scene.Scene`](https://compas.dev/compas/latest/) bound to
the `"Plotter"` context. `Plotter.add` delegates to it, so you get the full
COMPAS scene tree: parent/child relationships, composed world transformations,
and serialization — the same model used by the Rhino, Blender and Viewer
backends.

```python
from compas.geometry import Point, Translation
from compas_plotter import Plotter

plotter = Plotter()

parent = plotter.add(Point(0, 0, 0))
child = plotter.add(Point(1, 0, 0), parent=parent)

# Transforming the parent moves the child with it.
parent.transformation = Translation.from_vector([5, 0, 0])
assert child.worldtransformation[0, 3] == 5.0

plotter.scene  # -> the underlying PlotterScene
plotter.sceneobjects  # -> the plotter scene objects in the tree
```

Drawing is managed by the `Plotter` (objects are drawn when added, and
`Plotter.redraw` refreshes them), so you normally do not call `Scene.draw`
yourself.

## Saving

```python
plotter.save("figure.png", dpi=300)
```

## Dynamic plots and animations

[`Plotter.on`][compas_plotter.Plotter.on] turns a plotter into an animation
loop. The decorated function is called once per frame; mutate your geometry and
the plotter redraws it. Set `record` and `recording` to also export a GIF.

```python
from compas.geometry import Point
from compas_plotter import Plotter

plotter = Plotter()
point = Point(0, 0, 0)
plotter.add(point)
plotter.zoom_extents()

@plotter.on(interval=0.1, frames=50, record=True, recording="point.gif")
def move(frame):
    point.x = 0.1 * frame

plotter.show()
```

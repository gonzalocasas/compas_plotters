# COMPAS Plotters

![build](https://github.com/compas-dev/compas_plotter/workflows/build/badge.svg)
[![License](https://img.shields.io/github/license/compas-dev/compas_plotter.svg)](https://github.com/compas-dev/compas_plotter/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/compas_plotter.svg)](https://pypi.org/project/compas_plotter/)

**2D visualisation of COMPAS geometry and data structures, powered by matplotlib.**

`compas_plotter` provides a lightweight, dependency-free (other than matplotlib)
way to draw COMPAS objects in 2D. It is the COMPAS 2.x successor of the
`compas_plotters` package that shipped inside COMPAS up to version 1.17, rebuilt
on top of the modern [`compas.scene`](https://compas.dev/compas/latest/) system.
It registers a `"Plotter"` visualisation context, so any COMPAS object with a
registered plotter scene object can be drawn with a single `plotter.add(...)`.

## Installation

```bash
pip install compas_plotter
```

## Quick start

```python
from compas.geometry import Point, Line, Polygon
from compas.datastructures import Mesh
from compas_plotter import Plotter

plotter = Plotter(figsize=(8, 5))

mesh = Mesh.from_polyhedron(8)
plotter.add(mesh, show_vertices=True, show_edges=True)
plotter.add(Polygon([[0, 0, 0], [3, 0, 0], [3, 3, 0]]), facecolor=(0.9, 0.9, 1.0))
plotter.add(Line(Point(0, 0, 0), Point(3, 3, 0)), linecolor=(1, 0, 0))
plotter.add(Point(1.5, 1.5, 0))

plotter.zoom_extents()
plotter.show()
```

## Supported objects

| Category | Objects |
|---|---|
| Geometry | `Point`, `Vector`, `Line`, `Polyline`, `Polygon`, `Circle`, `Ellipse`, `Frame` |
| Shapes (drawn as XY projections) | `Box`, `Sphere`, `Cylinder`, `Cone`, `Capsule`, `Torus`, `Polyhedron` |
| Data structures | `Mesh`, `Graph` |

`Brep`, `Surface`, `NurbsCurve`, `VolMesh` and `Plane` are not yet supported —
see the [roadmap](#roadmap).

## Roadmap

Planned additions, most likely drawn as XY projections following the existing
`ShapeObject`:

- `Brep` and `Surface` (tessellate to a mesh, then project; `Brep` needs an
  optional backend such as `compas_occ`)
- `NurbsCurve` (sampled to a polyline)
- `VolMesh` and `Plane`

## Documentation

Full documentation is available at
[compas.dev/compas_plotter](https://compas.dev/compas_plotter).

## License

`compas_plotter` is released under the [MIT License](LICENSE).

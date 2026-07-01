# COMPAS Plotters

![build](https://github.com/compas-dev/compas_plotters/workflows/build/badge.svg)
[![License](https://img.shields.io/github/license/compas-dev/compas_plotters.svg)](https://github.com/compas-dev/compas_plotters/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/compas_plotters.svg)](https://pypi.org/project/compas_plotters/)

**2D visualisation of COMPAS geometry and data structures, powered by matplotlib.**

`compas_plotters` provides a lightweight, dependency-free (other than matplotlib)
way to draw COMPAS objects in 2D. It is the COMPAS 2.x successor of the
`compas_plotters` package that shipped inside COMPAS up to version 1.17, rebuilt
on top of the modern [`compas.scene`](https://compas.dev/compas/latest/) system.
It registers a `"Plotter"` visualisation context, so any COMPAS object with a
registered plotter scene object can be drawn with a single `plotter.add(...)`.

## Installation

```bash
pip install compas_plotters
```

## Quick start

```python
from compas.geometry import Point, Line, Polygon
from compas.datastructures import Mesh
from compas_plotters import Plotter

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
| Data structures | `Mesh`, `Graph` |

3D shapes (`Box`, `Sphere`, …), `Brep`, `Surface` and `VolMesh` are not yet
supported — see the [roadmap](https://compas.dev/compas_plotters).

## Documentation

Full documentation is available at
[compas.dev/compas_plotters](https://compas.dev/compas_plotters).

## License

`compas_plotters` is released under the [MIT License](LICENSE).

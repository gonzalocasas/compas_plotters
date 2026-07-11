# AGENTS.md

Guidance for AI coding agents (and humans) working on **compas_plotter**.
This is the canonical onboarding doc; `CLAUDE.md` just imports it.

## What this is

`compas_plotter` is the COMPAS 2.x revival of the 2D matplotlib visualisation
package that shipped inside COMPAS up to 1.17. It draws COMPAS geometry and data
structures onto a matplotlib canvas via the modern `compas.scene` system, by
registering a `"Plotter"` visualisation context — the same mechanism the Rhino,
Blender and Viewer backends use.

Status: **v0.1.0, pre-release.** Core is complete and working; not yet published
to PyPI and the GitHub repo may not exist yet.

## Architecture in 60 seconds

- **`Plotter`** ([src/compas_plotter/plotter.py](src/compas_plotter/plotter.py)) —
  wraps a matplotlib figure/axes. Public API: `add`, `add_from_list`, `find`,
  `zoom_extents`, `draw`, `redraw`, `show`, `save`, `pause`, `register_listener`,
  `on` (dynamic/animation + GIF).
- **`PlotterScene(compas.scene.Scene)`** ([scene/plotterscene.py](src/compas_plotter/scene/plotterscene.py)) —
  the container. Every `Plotter` owns one (`plotter.scene`), context hardcoded to
  `"Plotter"`. `Plotter.add` delegates to `PlotterScene.add`, which injects the
  owning plotter into each scene object and draws it. This gives a real scene tree
  (parent/child, composed `worldtransformation`) and serialization. Pattern copied
  from `compas_viewer`'s `ViewerScene`.
- **`PlotterSceneObject`** ([scene/plotterobject.py](src/compas_plotter/scene/plotterobject.py)) —
  base for all drawable objects. Subclasses implement `draw()` (returns the list
  of matplotlib artists, stored on `self._mpl_objects`) and `viewdata()` (the
  `[x, y]` points used by `zoom_extents`). `clear()` and `redraw()` are provided.
  Also exposes helpers `to_rgb()` and `to_color()`.
- **Registration** ([scene/__init__.py](src/compas_plotter/scene/__init__.py)) —
  `@plugin(category="factories") register_scene_objects()` maps each COMPAS type
  to its object with `register(T, O, context="Plotter")`. It is **also called
  eagerly at import** so the package works without entry-point discovery (editable
  installs). Drawing is managed by the `Plotter` (eager on add + `Plotter.redraw`);
  like the viewer, we do **not** rely on `Scene.draw()` in normal use.

## Supported objects

| Category | Objects |
|---|---|
| Geometry | Point, Vector, Line, Polyline, Polygon, Circle, Ellipse, Frame |
| Shapes (XY projection) | Box (dedicated), and Sphere / Cylinder / Cone / Capsule / Torus / Polyhedron via the shared `ShapeObject` |
| Data structures | Mesh, Graph (with vertex/edge/face and node/edge labels) |

**Not yet supported (roadmap):** Brep, Surface, NurbsCurve, VolMesh, Plane.

## Dev setup & commands

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"     # compas, matplotlib, pillow + dev tools
```

Common tasks (via `invoke`, configured in [tasks.py](tasks.py)):

```bash
invoke test        # pytest
invoke lint        # ruff check
invoke format      # ruff format + import sort
invoke docs        # build mkdocs site
```

Or directly:

```bash
pytest -q
ruff check src tests && ruff format --check src tests
python -m mkdocs serve      # live docs preview
```

> **Environment note:** the package needs a working numpy/matplotlib. If `import
> numpy`/`matplotlib` fails with a `libgfortran`/openblas dlopen error, your
> active (conda) environment is broken — create a fresh `venv` and install there.
> Tests set the matplotlib `Agg` backend in [conftest.py](conftest.py), so they
> run headless.

## Conventions

- **Python:** modern 3.9+ — `from __future__ import annotations`, native generics
  (`list[float] | None`), no Python-2 compat shims.
- **Docstrings:** numpy style, **fully type-hinted in signatures**, and **no
  redundant types repeated in the docstring** Parameters/Returns (mkdocstrings
  renders types from annotations). Match the existing scene objects.
- **Lint/format:** ruff (line-length 179, `select = E, F, I`, isort
  force-single-line). Keep `ruff check` and `ruff format --check` clean.
- **Changelog:** add an entry under `## Unreleased` in
  [CHANGELOG.md](CHANGELOG.md) for anything user-facing (CI enforces this on PRs).

## Gotchas (learned the hard way)

1. **Color descriptors coerce.** `SceneObject.color` / `GeometryObject.linecolor`
   etc. are descriptors whose setter runs `Color.coerce`, which **rejects mixed
   int/float rgb** like `(0.5, 0, 0.5)`. When assigning to one of these, wrap the
   value in `to_color(...)` (the `Color` constructor is lenient). Plain attributes
   you define yourself (`facecolor`, `edgecolor`, `size`, …) are unaffected — just
   convert with `to_rgb(...)` when handing them to matplotlib.
2. **matplotlib API drift.** Use `figure.add_subplot(1, 1, 1)`, not the string
   `"111"` (removed in mpl 3.11). Pin behaviour is tested across mpl versions in CI.
3. **Graph node size.** `GraphObject` default `sizepolicy="absolute"`
   (screen-constant, like mesh vertices); `"relative"` divides by node count and
   makes tiny graphs huge.
4. **Sub-object duplication.** Objects that spawn children during `draw()`
   (`Line`/`Polyline`/`Vector` with `draw_points=True`) will duplicate those
   children if `draw()` is re-run via `Scene.draw()`. Use `Plotter.redraw()`
   (the managed path) instead of calling `Scene.draw()` directly.

## Recipe: add a new scene object

There are two patterns already in the tree — copy the closest one.

**A. A single COMPAS type → dedicated object.** See
[scene/circleobject.py](src/compas_plotter/scene/circleobject.py) (geometry) or
[scene/boxobject.py](src/compas_plotter/scene/boxobject.py) (shape).

1. Create `scene/<thing>object.py` with
   `class <Thing>Object(PlotterSceneObject, GeometryObject)` (or `MeshObject` /
   `GraphObject` base for data structures).
2. Implement `__init__` (call `super().__init__(zorder=..., **kwargs)`; set your
   style attrs), `viewdata()`, and `draw()` (build matplotlib artists, append to
   `self._mpl_objects`, `return self._mpl_objects`).
3. In [scene/__init__.py](src/compas_plotter/scene/__init__.py): import it, add
   `register(<Thing>, <Thing>Object, context="Plotter")` inside
   `register_scene_objects()`, and add it to `__all__`.
4. Add a test in [tests/test_plotter.py](tests/test_plotter.py) and a CHANGELOG entry.

**B. A family of types → one shared object.** See
[scene/shapeobject.py](src/compas_plotter/scene/shapeobject.py): `ShapeObject`
tessellates any `Shape` with `to_vertices_and_faces()` and projects to XY; the
registration loop maps several classes to it.

### Next up (Brep/Surface)

Breps and surfaces are the main remaining gap. Plan: tessellate to a mesh
(`Brep.to_tesselation()` / surface sampling) and project to XY, mirroring
`ShapeObject`. Breps require an optional backend (e.g. `compas_occ`), so register
them inside a `try/except ImportError` block (see git history of
[scene/__init__.py](src/compas_plotter/scene/__init__.py) for the guarded pattern).

## Release

Versioning via `bump-my-version` ([pyproject.toml](pyproject.toml) `[tool.bumpversion]`,
which also bumps CITATION.cff and stamps the CHANGELOG). Tagging `v*` triggers
`.github/workflows/release.yml` (build across OS/Python, publish to PyPI).
Docs deploy from `main` via `.github/workflows/docs.yml` (mkdocs + mike).

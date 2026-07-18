# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Created `compas_plotter.__all_plugins__`, so COMPAS's plugin manager discovers the
  `register_scene_objects` factory through the standard `collect_all` path (the
  same mechanism `compas_viewer` uses).

### Changed

### Removed

* Removed Eager, import-time `register_scene_objects()` call in
  `compas_plotter.scene`, and the `from . import scene` side-effect import in
  `compas_plotter/__init__.py`. These populated COMPAS's global
  `ITEM_SCENEOBJECT` at import time, which suppressed the lazy
  `if not ITEM_SCENEOBJECT` discovery trigger in `compas.scene.context` and left
  every other backend unregistered.

## [1.0.0] 2026-07-11

### Added

### Changed

### Removed

## [1.0.0-rc0] 2026-07-11

### Added

* Initial COMPAS 2.x port of `compas_plotters` (the package that shipped inside COMPAS up to 1.17).
* `Plotter` class for 2D matplotlib visualisation, including dynamic plotting
  (`Plotter.on`) with optional GIF recording.
* `"Plotter"` visualisation context built on `compas.scene`.
* Scene objects for `Point`, `Vector`, `Line`, `Polyline`, `Polygon`, `Circle`,
  `Ellipse` and `Frame`.
* Scene objects for the `Mesh` and `Graph` data structures, with vertex/edge/face
  and node/edge labels.
* `PlotterScene`, a `compas.scene.Scene` subclass bound to the `"Plotter"`
  context. Every `Plotter` now owns one, giving a hierarchical scene tree
  (parent/child transforms), serialization, and API symmetry with the Rhino,
  Blender and Viewer backends.
* Scene object for `Box`, drawn as the exact XY projection of its six faces.
* Shared `ShapeObject` drawing `Sphere`, `Cylinder`, `Cone`, `Capsule`, `Torus`
  and `Polyhedron` as tessellated XY projections, with `u`/`v` resolution control.

### Changed

* `GraphObject.node_xyz` and `MeshObject.vertex_xyz` return fresh view
  coordinates on every access instead of a mapping cached at first access, so
  a redraw in a `Plotter.on` animation loop picks up
  changes to the coordinates of the underlying datastructure.

### Removed

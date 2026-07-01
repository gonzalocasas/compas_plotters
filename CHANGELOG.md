# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Initial COMPAS 2.x port of `compas_plotters`.
* `Plotter` class for 2D matplotlib visualisation, including dynamic plotting
  (`Plotter.on`) with optional GIF recording.
* `"Plotter"` visualisation context built on `compas.scene`.
* Scene objects for `Point`, `Vector`, `Line`, `Polyline`, `Polygon`, `Circle`,
  `Ellipse` and `Frame`.
* Scene objects for the `Mesh` and `Graph` data structures, with vertex/edge/face
  and node/edge labels.

### Changed

### Removed

# API Reference

The public API of `compas_plotters` is small:

- **[compas_plotters](compas_plotters.md)** — the [`Plotter`][compas_plotters.Plotter]
  class, the main entry point for building 2D plots.
- **[compas_plotters.scene](compas_plotters.scene.md)** — the `"Plotter"`
  visualisation-context scene objects, one per supported COMPAS type. You rarely
  instantiate these directly; `Plotter.add` creates them for you.

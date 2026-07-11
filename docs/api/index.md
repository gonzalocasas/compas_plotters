# API Reference

The public API of `compas_plotter` is small:

- **[compas_plotter](compas_plotter.md)** — the [`Plotter`][compas_plotter.Plotter]
  class, the main entry point for building 2D plots.
- **[compas_plotter.scene](compas_plotter.scene.md)** — the `"Plotter"`
  visualisation-context scene objects, one per supported COMPAS type. You rarely
  instantiate these directly; `Plotter.add` creates them for you.

# Installation

## Stable

Install the latest stable release from PyPI:

```bash
pip install compas_plotters
```

This pulls in `compas` and `matplotlib` (plus `pillow` for GIF recording).

## Conda

If you manage your COMPAS environment with conda, install the dependencies from
conda-forge and `compas_plotters` from pip:

```bash
conda create -n compas-env python=3.12 compas matplotlib pillow
conda activate compas-env
pip install compas_plotters
```

## Latest (development)

Install the latest version directly from the git repository:

```bash
pip install git+https://github.com/compas-dev/compas_plotters.git
```

## From source

Clone the repository and install it in editable mode with the development
dependencies:

```bash
git clone https://github.com/compas-dev/compas_plotters.git
cd compas_plotters
pip install -e ".[dev]"
```

## Verify

```python
import compas_plotters
print(compas_plotters.__version__)
```

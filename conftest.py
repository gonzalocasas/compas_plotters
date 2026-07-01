import matplotlib


def pytest_configure(config):
    # Always use a non-interactive backend during tests so they run headless.
    matplotlib.use("Agg")

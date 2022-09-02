import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runeph", action="store_true", default=False, help="run ephemeris tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "eph: mark test as ephemeris test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runeph"):
        # --runeph given in cli: do not skip slow tests
        return
    skip_eph = pytest.mark.skip(reason="need --runeph option to run")
    for item in items:
        if "eph" in item.keywords:
            item.add_marker(skip_eph)

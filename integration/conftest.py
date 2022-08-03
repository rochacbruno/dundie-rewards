# conftest.py
MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


"""def pytest_configure(config):
    # mode funcinal
    map(
        lambda line: config.addinivalue_line('markers', line), MARKER.split("\n")
    )
"""

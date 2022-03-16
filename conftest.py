import pytest
from unittest.mock import patch


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


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):  # injeção de dependencias
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield  # protocolo de generators


@pytest.fixture(autouse=True, scope="function")
def setup_testing_database(request):
    """For each test, create a database file on tmpdir
    force database.py to use that filepath.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.json"))
    with patch("dundie.database.DATABASE_PATH", test_db):
        yield

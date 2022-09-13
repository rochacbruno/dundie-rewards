<<<<<<< HEAD
=======
"""Conftest."""

>>>>>>> projeto-dundie-rewards/main
import warnings
import pytest
from unittest.mock import patch
from sqlmodel import create_engine
from dundie import models
from sqlalchemy.exc import SAWarning


warnings.filterwarnings("ignore", category=SAWarning)


MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""


def pytest_configure(config):
<<<<<<< HEAD
=======
    """access_allowed()"""
>>>>>>> projeto-dundie-rewards/main
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):  # injeção de dependencias
<<<<<<< HEAD
=======
    """access_allowed()"""
>>>>>>> projeto-dundie-rewards/main
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield  # protocolo de generators


@pytest.fixture(autouse=True, scope="function")
def setup_testing_database(request):
<<<<<<< HEAD
    """For each test, create a database file on tmpdir
    force database.py to use that filepath.
    """
=======
    """For each test, create a database file on tmpdir force database."""
    """py to use that filepath."""
>>>>>>> projeto-dundie-rewards/main
    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.db"))
    engine = create_engine(f"sqlite:///{test_db}")
    models.SQLModel.metadata.create_all(bind=engine)
    with patch("dundie.database.engine", engine):
        yield

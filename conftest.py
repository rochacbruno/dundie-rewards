from io import StringIO
import warnings
import pytest
from unittest.mock import patch
from sqlmodel import create_engine
from dundie import models
from sqlalchemy.exc import SAWarning
from decouple import Config, RepositoryEnv


warnings.filterwarnings("ignore", category=SAWarning)


MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""

ENVFILE = '''
DUNDIE_USER=True
DUNDIE_PASSWORD=True
DUNDIE_FALSE=False
'''


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
    test_db = str(tmpdir.join("database.test.db"))
    engine = create_engine(f"sqlite:///{test_db}")
    models.SQLModel.metadata.create_all(bind=engine)
    with patch("dundie.database.engine", engine):
        yield


@pytest.fixture(autouse=True, scope="function")
def setup_testing_env(request):
    """For each test, set the environment variable
    to an empty string.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    test_env = str(tmpdir.join("env.test"))
    with patch("dundie.core.VAR_ENV", test_env):
        yield


@pytest.fixture(scope="module")
def config():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        return Config(RepositoryEnv('.env'))
#

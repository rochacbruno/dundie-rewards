import pytest


@pytest.mark.unit
def test_negative_access_allowed(config):
    assert False is config("DUNDIE_FALSE", cast=bool)


@pytest.mark.unit
def test_positive_access_allowed(config):
    assert True is config("DUNDIE_USER", cast=bool)

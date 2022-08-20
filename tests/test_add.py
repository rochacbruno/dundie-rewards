import pytest

from dundie.core import add
from dundie.database import add_person, commit, connect


@pytest.mark.unit
def test_add_movement():
    pk = "joe@doe.com"
    data = {"role": "Salesman", "dept": "Sale", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    pk = "jim@doe.com"
    data = {"role": "Manager", "dept": "Management", "name": "Jim Doe"}
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    add(-30, email="joe@doe.com")
    add(90, dept="Management")

    db = connect()
    assert db["balance"]["joe@doe.com"] == 470
    assert db["balance"]["jim@doe.com"] == 190

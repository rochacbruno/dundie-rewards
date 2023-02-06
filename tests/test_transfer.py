import os

import pytest

from dundie.core import transfer
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person


@pytest.mark.unit
def test_transfer():
    with get_session() as session:
        joe = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance_joe = Person(**joe)
        _, created = add_person(session=session, instance=instance_joe)
        assert created is True

        jim = {
            "email": "jim@doe.com",
            "name": "Jim Doe",
            "dept": "Management",
            "role": "Manager",
        }

        instance_jim = Person(**jim)
        _, created = add_person(session=session, instance=instance_jim)
        assert created is True

        session.commit()

        os.environ["DUNDIE_USER"] = "joe@doe.com"

        transfer(90, to="jim@doe.com")

        os.environ["DUNDIE_USER"] = "jim@doe.com"

        transfer(100, to="joe@doe.com")

        assert instance_joe.balance[0].value == 510
        assert instance_jim.balance[0].value == 90

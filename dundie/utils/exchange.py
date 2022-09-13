<<<<<<< HEAD
=======
"""Utility API for convertion currency."""

>>>>>>> projeto-dundie-rewards/main
from decimal import Decimal
from typing import Dict, List

import httpx
from pydantic import BaseModel, Field

from dundie.settings import API_BASE_URL


class USDRate(BaseModel):
<<<<<<< HEAD
=======
    """..."""

>>>>>>> projeto-dundie-rewards/main
    code: str = Field(default="USD")
    codein: str = Field(default="USD")
    name: str = Field(default="Dolar/Dolar")
    value: Decimal = Field(alias="high")


def get_rates(currencies: List[str]) -> Dict[str, USDRate]:
<<<<<<< HEAD
    """Gets current rate for USD vs Currency"""
=======
    """Get the current rates of dolar in each currency."""
>>>>>>> projeto-dundie-rewards/main
    return_data = {}
    for currency in currencies:
        if currency == "USD":
            return_data[currency] = USDRate(high=1)
        else:
            response = httpx.get(API_BASE_URL.format(currency=currency))
            if response.status_code == 200:
<<<<<<< HEAD
                data = response.json()["USD"]
                return_data[currency] = USDRate(**data)
            else:
                return_data[currency] = USDRate(name="api/error", high=0)

=======
                data = response.json()["USD" + currency]
                return_data[currency] = USDRate(**data)
            else:
                return_data[currency] = USDRate(name="Api/Error", high=0)
>>>>>>> projeto-dundie-rewards/main
    return return_data

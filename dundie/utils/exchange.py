import httpx
from decimal import Decimal
from typing import List, Dict
from dundie.settings import API_BASE_URL
from pydantic import BaseModel, Field


class USDRate(BaseModel):
    code: str = Field(default="USD")
    codein: str = Field(default="USD")
    name: str = Field(default="Dolar/Dolar")
    value: Decimal = Field(alias="high")


def get_rates(currencies: List[str]) -> Dict[str, USDRate]:
    """Gets the current rates of dolar in each currency"""
    return_data = {}
    for currency in currencies:
        if currency == "USD":
            return_data[currency] = USDRate(high=1)
        else:
            response = httpx.get(API_BASE_URL.format(currency=currency))
            if response.status_code == 200:
                data = response.json()["USD"]
                return_data[currency] = USDRate(**data)
            else:
                return_data[currency] = USDRate(name="Api/Error", high=0)
    return return_data

import pytest

from dundie.utils.exchange import get_rates


@pytest.mark.unit
@pytest.mark.enable_socket
def test_exchange_positive():
    # TODO: Make exchange call negative connection
    currency_USD = ["USD"]
    currency_BRL = ["BRL"]

    result_USD = get_rates(currencies=currency_USD)
    result_BRL = get_rates(currencies=currency_BRL)

    assert result_USD.get("USD").codein == "USD"
    assert result_BRL.get("BRL").codein == "BRL"
    assert result_USD.get("USD").name == "Dolar/Dolar"
    assert result_BRL.get("BRL").name == "Dólar Americano/Real Brasileiro"
    assert result_USD.get("USD").value == 1
    assert result_BRL.get("BRL").value > 1

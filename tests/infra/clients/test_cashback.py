from app.infra.clients.cashback import CashbackClient
import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("token", "DUMMY")],
    }


@pytest.mark.vcr()
def test_get_cashback_acumulado():
    client = CashbackClient()
    assert client.get_cashback_acumulado(cpf="123456") == 2009


@pytest.mark.vcr()
def test_get_cashback_acumulado_raises_error_with_no_cpf():
    with pytest.raises(Exception, match="Informe o CPF do revendedor\(a\)!"):
        client = CashbackClient()
        client.get_cashback_acumulado(cpf=None)

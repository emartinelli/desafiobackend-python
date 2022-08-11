import pytest

from app.services.cashback import CashbackService


@pytest.mark.parametrize(
    "cpf, expected_cashback_acumulado",
    [
        ("12345678901", 123.45),
    ],
)
def test_get_cashback_acumulado(mocker, cpf, expected_cashback_acumulado):
    mocker.patch(
        "app.infra.clients.cashback.CashbackClient.get_cashback_acumulado",
        return_value=expected_cashback_acumulado,
    )
    service = CashbackService()

    assert service.get_cashback_acumulado(cpf=cpf) == expected_cashback_acumulado

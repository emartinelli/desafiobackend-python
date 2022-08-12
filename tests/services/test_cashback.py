import pytest
from sqlalchemy.orm import Session

from app.exceptions.revendedor import RevendedorNotFoundException
from app.schemas.revendedor import RevendedorIn
from app.services.cashback import CashbackService
from tests import utils


@pytest.mark.parametrize(
    "revendedor_in, expected_cashback_acumulado",
    [
        (
            RevendedorIn(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            123.45,
        ),
    ],
)
def test_get_cashback_acumulado(
    db_session: Session,
    mocker,
    revendedor_in: RevendedorIn,
    expected_cashback_acumulado: float,
):
    mocker.patch(
        "app.infra.clients.cashback.CashbackClient.get_cashback_acumulado",
        return_value=expected_cashback_acumulado,
    )
    utils.create_revendedor(db_session, revendedor_in)

    service = CashbackService(db_session)
    service.get_cashback_acumulado(cpf=revendedor_in.cpf)


@pytest.mark.parametrize(
    "cpf, expected_cashback_acumulado",
    [
        ("12345678901", 123.45),
    ],
)
def test_get_cashback_acumulado(
    db_session: Session, mocker, cpf, expected_cashback_acumulado
):
    mocker.patch(
        "app.infra.clients.cashback.CashbackClient.get_cashback_acumulado",
        return_value=expected_cashback_acumulado,
    )
    service = CashbackService(db_session)

    with pytest.raises(RevendedorNotFoundException):
        service.get_cashback_acumulado(cpf=cpf)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infra.settings import settings
from app.schemas.revendedor import RevendedorIn
from tests import utils


@pytest.mark.parametrize(
    "revendedor_in, compra_in, compra_out",
    [
        (
            dict(
                nome_completo="Teste Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            dict(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor="100.00",
                data="2020-01-01 00:00:00",
                cpf_revendedor="12345678901",
            ),
            dict(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor=100.00,
                data="2020-01-01T00:00:00",
                porcentagem_de_cashback=0.1,
                valor_de_cashback=10.00,
                status="Em validação",
            ),
        )
    ],
)
def test_create_compra(
    client: TestClient,
    db_session: Session,
    revendedor_in: dict,
    compra_in: dict,
    compra_out: dict,
):
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.post(
        f"{settings.API_V1_STR}/compra/",
        json=compra_in,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201
    assert response.json() == compra_out

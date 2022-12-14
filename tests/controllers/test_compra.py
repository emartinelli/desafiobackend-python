import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infra.settings import settings
from app.schemas.compra import CompraIn
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
                porcentagem_de_cashback=None,
                valor_de_cashback=None,
                status="Em validação",
            ),
        )
    ],
)
def test_create_compra(
    client: TestClient,
    db_session: Session,
    api_user_headers: dict[str, str],
    revendedor_in: dict,
    compra_in: dict,
    compra_out: dict,
):
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.post(
        f"{settings.API_V1_STR}/compra/",
        json=compra_in,
        headers={"Content-Type": "application/json", **api_user_headers},
    )

    assert response.status_code == 201
    assert response.json() == compra_out


@pytest.mark.parametrize(
    "revendedor_in, compra_in, error_message",
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
            "Compra já cadastrada",
        )
    ],
)
def test_create_compra_that_already_exists_returns_422(
    client: TestClient,
    db_session: Session,
    api_user_headers: dict[str, str],
    revendedor_in: dict,
    compra_in: dict,
    error_message: str,
):
    utils.create_revendedor_and_compra(
        db_session, CompraIn(**compra_in), RevendedorIn(**revendedor_in)
    )

    response = client.post(
        f"{settings.API_V1_STR}/compra/",
        json=compra_in,
        headers={"Content-Type": "application/json", **api_user_headers},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == error_message


@pytest.mark.parametrize(
    "compra_in, error_message",
    [
        (
            dict(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor="100.00",
                data="2020-01-01 00:00:00",
                cpf_revendedor="12345678901",
            ),
            "Nenhum revendedor encontrado com o CPF `12345678901`",
        )
    ],
)
def test_create_compra_with_no_related_revendedor_returns_422(
    client: TestClient,
    api_user_headers: dict[str, str],
    compra_in: dict,
    error_message: str,
):
    response = client.post(
        f"{settings.API_V1_STR}/compra/",
        json=compra_in,
        headers={"Content-Type": "application/json", **api_user_headers},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == error_message

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infra.settings import settings
from app.schemas.revendedor import RevendedorIn
from tests import utils


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("token", "DUMMY")],
    }


@pytest.mark.parametrize(
    "revendedor_in, revendedor_out",
    [
        (
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
            ),
        )
    ],
)
def test_create_revendedor(
    client: TestClient, revendedor_in: dict, revendedor_out: dict
):
    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201
    assert response.json() == revendedor_out


@pytest.mark.parametrize(
    "revendedor_in, error_message",
    [
        (
            dict(
                nome_completo="Teste Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            "Revendedor já cadastrado",
        )
    ],
)
def test_create_revendedor_that_already_exists_returns_422(
    client: TestClient, db_session: Session, revendedor_in: dict, error_message: str
):
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == error_message


@pytest.mark.parametrize(
    "revendedor_in, error_message",
    [
        (
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="invalid_email",
                senha="123456",
            ),
            "value is not a valid email address",
        ),
        (
            dict(
                nome_completo="Teste",
                cpf="12",
                email="teste@teste.com",
                senha="123456",
            ),
            "CPF deve conter 11 dígitos",
        ),
    ],
)
def test_create_revendedor_with_invalid_data_input_returns_422(
    client: TestClient, revendedor_in: dict, error_message: str
):
    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == error_message


@pytest.mark.parametrize(
    "revendedor_in, revendedor_out",
    [
        (
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
            ),
        )
    ],
)
@pytest.mark.vcr
def test_get_cashback_acumulado(
    client: TestClient, db_session: Session, revendedor_in: dict, revendedor_out: dict
):
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.get(
        f"{settings.API_V1_STR}/revendedor/{revendedor_in['cpf']}/cashback",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json()["revendedor"] == revendedor_out
    assert response.json()["cashback_acumulado"] == 3096

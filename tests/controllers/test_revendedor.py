import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infra.settings import settings
from app.schemas.compra import CompraIn
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
    client: TestClient,
    api_user_headers: dict[str, str],
    revendedor_in: dict,
    revendedor_out: dict,
):
    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json", **api_user_headers},
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
    client: TestClient,
    db_session: Session,
    api_user_headers: dict[str, str],
    revendedor_in: dict,
    error_message: str,
):
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json", **api_user_headers},
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
    client: TestClient,
    api_user_headers: dict[str, str],
    revendedor_in: dict,
    error_message: str,
):
    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json", **api_user_headers},
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
    client: TestClient,
    db_session: Session,
    api_user_headers: dict[str, str],
    revendedor_in: dict,
    revendedor_out: dict,
):
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.get(
        f"{settings.API_V1_STR}/revendedor/{revendedor_in['cpf']}/cashback",
        headers={"Content-Type": "application/json", **api_user_headers},
    )

    assert response.status_code == 200
    assert response.json()["revendedor"] == revendedor_out
    assert response.json()["cashback_acumulado"] == 3096


@pytest.mark.parametrize(
    "revendedor_in",
    [
        (
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            )
        )
    ],
)
def test_get_access_token(
    client: TestClient,
    db_session: Session,
    revendedor_in: dict,
) -> None:
    login_data = {
        "username": revendedor_in["email"],
        "password": revendedor_in["senha"],
    }
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    response = client.post(
        f"{settings.API_V1_STR}/revendedor/login/access-token", data=login_data
    )
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


@pytest.mark.parametrize(
    "revendedor_in",
    [
        (
            dict(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            )
        )
    ],
)
def test_validate_login(
    client: TestClient, db_session: Session, make_revendedor_headers, revendedor_in
) -> None:
    utils.create_revendedor(db_session, RevendedorIn(**revendedor_in))

    r = client.get(
        f"{settings.API_V1_STR}/revendedor/login/validate",
        headers=make_revendedor_headers(revendedor_in["email"], revendedor_in["senha"]),
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


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
def test_get_compras(
    client: TestClient,
    db_session: Session,
    revendedor_in: dict,
    api_user_headers: dict[str, str],
    compra_in: dict,
    compra_out: dict,
):
    utils.create_revendedor_and_compra(
        db_session, CompraIn(**compra_in), RevendedorIn(**revendedor_in)
    )

    response = client.get(
        f"{settings.API_V1_STR}/revendedor/{revendedor_in['cpf']}/compras/",
        json=compra_in,
        headers={"Content-Type": "application/json", **api_user_headers},
    )

    assert response.status_code == 200
    assert compra_out in response.json()["items"]

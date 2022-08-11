import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infra.settings import settings


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

    assert response.status_code == 200
    assert response.json() == revendedor_out


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
def test_create_revendedor_that_already_exists_raises_exception(
    client: TestClient, revendedor_in: dict, revendedor_out: dict
):
    response = client.post(
        f"{settings.API_V1_STR}/revendedor/",
        json=revendedor_in,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json() == revendedor_out

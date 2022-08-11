import pytest
from sqlalchemy.orm import Session
from app.repository.revendedor import RevendedorRepository

from app.schemas.compra import CompraIn, CompraOut
from app.schemas.revendedor import RevendedorIn
from app.services.compra import CompraService


@pytest.mark.parametrize(
    "compra_in, compra_out",
    [
        (
            CompraIn(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor="100.00",
                data="2020-01-01",
                cpf_revendedor="12345678901",
            ),
            CompraOut(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor="100.00",
                data="2020-01-01",
                porcentagem_de_cashback="0.10",
                valor_de_cashback="10.00",
                status="Em validação",
            ),
        )
    ],
)
def test_compra_create(db_session: Session, compra_in: CompraIn, compra_out: CompraOut):
    RevendedorRepository(db_session).create(
        RevendedorIn(
            nome_completo="Teste",
            cpf=compra_in.cpf_revendedor,
            email="teste@teste.com",
            senha="123456",
        )
    )

    service = CompraService(db_session)
    compra = service.create(compra_in)

    assert compra == compra_out

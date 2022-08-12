import datetime
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.repositories.revendedor import RevendedorRepository
from app.schemas.compra import CompraIn, CompraOut, StatusEnum
from app.schemas.revendedor import RevendedorIn
from app.services.compra import CompraService
from tests import utils


@pytest.mark.parametrize(
    "compra_in, compra_out",
    [
        (
            CompraIn(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor=Decimal("100.00"),
                data=datetime.datetime(2020, 1, 1),
                cpf_revendedor="12345678901",
            ),
            CompraOut(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor=Decimal("100.00"),
                data=datetime.datetime(2020, 1, 1),
                porcentagem_de_cashback=Decimal("0.10"),
                valor_de_cashback=Decimal("10.00"),
                status=StatusEnum.em_validacao,
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


@pytest.mark.parametrize(
    "compra_in",
    [
        CompraIn(
            codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
            valor=Decimal("100.00"),
            data=datetime.datetime(2020, 1, 1),
            cpf_revendedor="12345678901",
        ),
    ],
)
def test_compra_create_raises_exception_when_revendedor_does_exist(
    db_session: Session,
    compra_in: CompraIn,
):
    service = CompraService(db_session)

    with pytest.raises(
        Exception,
        match=f"Revendedor with given cpf `{compra_in.cpf_revendedor}` does not exist",
    ):
        service.create(compra_in)


@pytest.mark.parametrize(
    "revendedor_in, compra_in, compras_out",
    [
        (
            RevendedorIn(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            CompraIn(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor=Decimal("100.00"),
                data=datetime.datetime(2020, 1, 1),
                cpf_revendedor="12345678901",
            ),
            [
                CompraOut(
                    codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                    valor=Decimal("100.00"),
                    data=datetime.datetime(2020, 1, 1),
                    porcentagem_de_cashback=Decimal("0.10"),
                    valor_de_cashback=Decimal("10.00"),
                    status=StatusEnum.em_validacao,
                ),
            ],
        )
    ],
)
def test_get_compras(
    db_session: Session,
    revendedor_in: RevendedorIn,
    compra_in: CompraIn,
    compras_out: list[CompraOut],
):
    utils.create_revendedor(db_session, revendedor_in)
    service = CompraService(db_session)
    service.create(compra_in)

    compras = service.get_compras()

    assert compras == compras_out

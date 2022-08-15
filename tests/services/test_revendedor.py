import datetime
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.repositories.revendedor import DuplicateRevendedorException
from app.schemas.compra import CompraIn, CompraOut, StatusEnum
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.services.revendedor import RevendedorService
from tests import utils


@pytest.mark.parametrize(
    "revendedor_in, revendedor_out",
    [
        (
            RevendedorIn(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
                senha="123456",
            ),
            RevendedorOut(
                nome_completo="Teste",
                cpf="12345678901",
                email="teste@teste.com",
            ),
        )
    ],
)
def test_revendedor_create(
    db_session: Session, revendedor_in: RevendedorIn, revendedor_out: RevendedorOut
):
    service = RevendedorService(db_session)
    revendedor = service.create(revendedor_in)

    assert revendedor == revendedor_out


@pytest.mark.parametrize(
    "revendedor_in",
    [
        RevendedorIn(
            nome_completo="Teste",
            cpf="12345678901",
            email="teste@teste.com",
            senha="123456",
        )
    ],
)
def test_revendedor_create_that_already_exists_raises_exception(
    db_session: Session, revendedor_in: RevendedorIn
):
    utils.create_revendedor(db_session, revendedor_in)
    service = RevendedorService(db_session)

    with pytest.raises(
        DuplicateRevendedorException, match="Revendedor using same information"
    ):
        service.create(revendedor_in)


@pytest.mark.parametrize(
    "revendedor_in, compra_in, compra_out",
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
            CompraOut(
                codigo="ffedaf47-4fc5-4185-8ad1-003930d316e8",
                valor=Decimal("100.00"),
                data=datetime.datetime(2020, 1, 1),
                status=StatusEnum.em_validacao,
                porcentagem_de_cashback=Decimal("0.10"),
                valor_de_cashback=Decimal("10.00"),
            ),
        )
    ],
)
def test_get_compras(
    db_session: Session,
    cashback_criterios: None,
    revendedor_in: RevendedorIn,
    compra_in: dict,
    compra_out: dict,
):
    utils.create_revendedor_and_compra(
        db_session, revendedor_in=revendedor_in, compra_in=compra_in
    )

    service = RevendedorService(db_session)
    compras = service.get_compras(revendedor_in.cpf)
    assert compra_out in compras

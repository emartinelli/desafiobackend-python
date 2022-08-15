import datetime
import uuid
from decimal import Decimal

import pytest
from psycopg2.extras import NumericRange
from sqlalchemy.orm import Session

from app.models.cashback import CashbackCriterio
from app.repositories.revendedor import DuplicateRevendedorException
from app.schemas.compra import CompraIn, CompraOut, StatusEnum
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.services.revendedor import RevendedorService
from tests import utils


@pytest.fixture
def cashback_criterios(db_session: Session) -> None:
    db_session.add_all(
        [
            CashbackCriterio(
                intervalo=NumericRange(Decimal("0"), Decimal("1000")),
                porcentagem_de_cashback=Decimal("0.10"),
            ),
            CashbackCriterio(
                intervalo=NumericRange(Decimal("1000"), Decimal("1500")),
                porcentagem_de_cashback=Decimal("0.10"),
            ),
            CashbackCriterio(
                intervalo=NumericRange(
                    Decimal("1500"),
                ),
                porcentagem_de_cashback=Decimal("0.10"),
            ),
        ]
    )
    db_session.commit()


@pytest.fixture
def revendedor_in() -> RevendedorIn:
    return RevendedorIn(
        nome_completo="Teste",
        cpf="12345678901",
        email="teste@teste.com",
        senha="123456",
    )


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
    "compras_data_in, compras_data_out",
    [
        (
            [
                dict(
                    valor=Decimal("100.00"),
                    data=datetime.datetime(2020, 1, 1),
                )
            ],
            [
                dict(
                    valor=Decimal("100.00"),
                    data=datetime.datetime(2020, 1, 1),
                    porcentagem_de_cashback=Decimal("0.10"),
                    valor_de_cashback=Decimal("10.00"),
                )
            ],
        )
    ],
)
def test_get_compras(
    db_session: Session,
    cashback_criterios: None,
    revendedor_in: RevendedorIn,
    compras_data_in: dict,
    compras_data_out: dict,
):
    utils.create_revendedor(db_session, revendedor_in=revendedor_in)

    CompraIn(codigo=uuid.uuid4(), cpf_revendedor=revendedor_in.cpf, **compra_in),

    for compra_in in compras_data_in:
        utils.create_compra(
            db_session,
            compra_in=CompraIn(
                codigo=uuid.uuid4(), cpf_revendedor=revendedor_in.cpf, **compra_in
            ),
        )

    service = RevendedorService(db_session)
    compras = service.get_compras(revendedor_in.cpf)

    for compra_out, compra_data_in in zip(compras, compras_data_in):
        assert compra_out == CompraOut()

import pytest
from sqlalchemy.orm import Session

from app.repositories.revendedor import DuplicateRevendedorException
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

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.compra import Compra as CompraModel
from app.models.revendedor import Revendedor as RevendedorModel
from app.repositories.compra import CompraRepository
from app.repositories.revendedor import RevendedorRepository
from app.schemas.compra import CompraIn
from app.schemas.revendedor import RevendedorIn


def create_revendedor(db: Session, revendedor_in: RevendedorIn) -> RevendedorModel:
    return RevendedorRepository(db).create(revendedor_in)


def create_compra(
    db: Session,
    compra_in: CompraIn,
    revendedor_model: RevendedorModel,
    porcentagem_de_cashback: Decimal,
) -> CompraModel:
    return CompraRepository(db).create(
        compra_in,
        revendedor_id=revendedor_model,
        porcentagem_de_cashback=porcentagem_de_cashback,
    )

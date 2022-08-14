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


def create_revendedor_and_compra(
    db: Session,
    compra_in: CompraIn,
    revendedor_in: RevendedorIn,
) -> CompraModel:
    revendedor = create_revendedor(db, revendedor_in)
    return CompraRepository(db).create(compra_in, revendedor_id=revendedor.id)

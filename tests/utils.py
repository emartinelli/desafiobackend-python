from sqlalchemy.orm import Session

from app.repositories.revendedor import RevendedorRepository
from app.schemas.revendedor import RevendedorIn, RevendedorOut


def create_revendedor(db: Session, revendedor_in: RevendedorIn) -> RevendedorOut:
    return RevendedorRepository(db).create(revendedor_in)

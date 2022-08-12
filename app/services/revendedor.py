from sqlalchemy.orm import Session

from app.repositories.revendedor import RevendedorRepository
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.models.revendedor import Revendedor as RevendedorModel


class RevendedorService:
    def __init__(self, db: Session):
        self.repository = RevendedorRepository(db)

    def create(self, revendedor: RevendedorIn) -> RevendedorOut:
        revendedor_model = self.repository.create(revendedor)
        return RevendedorRepository.map_model_to_schema(revendedor_model)

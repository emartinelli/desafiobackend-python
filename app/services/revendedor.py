from sqlalchemy.orm import Session

from app.models.revendedor import Revendedor as RevendedorModel
from app.repository.revendedor import RevendedorRepository
from app.schemas.revendedor import RevendedorIn, RevendedorOut


class RevendedorService:
    def __init__(self, db: Session):
        self.repository = RevendedorRepository(db)

    def create(self, revendedor: RevendedorIn) -> RevendedorOut:
        revendedor_model = self.repository.create(revendedor)

        return RevendedorOut(
            nome_completo=revendedor_model.nome_completo,
            cpf=revendedor_model.cpf,
            email=revendedor_model.email,
        )

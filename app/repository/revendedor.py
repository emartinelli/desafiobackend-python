from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.revendedor import Revendedor as RevendedorModel
from app.schemas.revendedor import RevendedorIn


class DuplicateRevendedorException(Exception):
    pass


class RevendedorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, revendedor: RevendedorIn) -> RevendedorModel:
        revendedor_model = RevendedorModel(
            cpf=revendedor.cpf,
            email=revendedor.email,
            nome_completo=revendedor.nome_completo,
            senha_com_hash=revendedor.senha,
        )

        self.db.add(revendedor_model)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateRevendedorException(
                "Revendedor using same information"
            ) from e

        self.db.refresh(revendedor_model)

        return revendedor_model

    def get_revendedor_by_cpf(self, cpf: str) -> RevendedorModel:
        return self.db.query(RevendedorModel).filter(RevendedorModel.cpf == cpf).first()

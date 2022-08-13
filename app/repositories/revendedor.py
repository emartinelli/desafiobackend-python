from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.revendedor import DuplicateRevendedorException
from app.models.revendedor import Revendedor as RevendedorModel
from app.schemas.revendedor import RevendedorIn, RevendedorOut


class RevendedorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, revendedor: RevendedorIn) -> RevendedorModel:
        revendedor_model = RevendedorModel(
            cpf=revendedor.cpf,
            email=revendedor.email,
            nome_completo=revendedor.nome_completo,
            senha_com_hash=revendedor.senha,
            status_compra_default=revendedor.status_compra_default,
        )

        self.db.add(revendedor_model)
        try:
            self.db.commit()
        except IntegrityError as e:
            raise DuplicateRevendedorException(
                "Revendedor using same information"
            ) from e

        self.db.refresh(revendedor_model)

        return revendedor_model

    def get_revendedor_by_cpf(self, cpf: str) -> RevendedorModel:
        return self.db.query(RevendedorModel).filter(RevendedorModel.cpf == cpf).first()

    @classmethod
    def map_model_to_schema(cls, model: RevendedorModel) -> RevendedorOut:
        return RevendedorOut(
            nome_completo=model.nome_completo,
            cpf=model.cpf,
            email=model.email,
        )

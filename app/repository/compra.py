from uuid import UUID
from sqlalchemy.orm import Session

from app.models.compra import Compra as CompraModel
from app.schemas.compra import CompraIn, CompraOut


class CompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, compra: CompraIn, revendedor_id: UUID) -> CompraModel:
        compra_model = CompraModel(
            codigo=compra.codigo,
            valor=compra.valor,
            data=compra.data,
            revendedor_id=revendedor_id,
        )

        self.db.add(compra_model)
        self.db.commit()
        self.db.refresh(compra_model)

        return compra_model

    def get_all(self) -> list[CompraModel]:
        return self.db.query(CompraModel).all()

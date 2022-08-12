from decimal import Decimal
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.compra import DuplicateCompraException
from app.models.compra import Compra as CompraModel
from app.schemas.compra import CompraIn, CompraOut


class CompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, compra: CompraIn, revendedor_id: UUID, porcentagem_de_cashback: Decimal
    ) -> CompraModel:
        compra_model = CompraModel(
            codigo=compra.codigo,
            valor=compra.valor,
            data=compra.data,
            revendedor_id=revendedor_id,
            porcentagem_de_cashback=porcentagem_de_cashback,
        )

        self.db.add(compra_model)
        try:
            self.db.commit()
        except IntegrityError as e:
            raise DuplicateCompraException(
                f"Compra with given codigo `{compra.codigo}` already exists"
            ) from e
        self.db.refresh(compra_model)

        return compra_model

    def get_all(self) -> list[CompraModel]:
        return self.db.query(CompraModel).all()

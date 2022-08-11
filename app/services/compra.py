from sqlalchemy.orm import Session

from app.models.compra import Compra as CompraModel
from app.repository.compra import CompraRepository
from app.repository.revendedor import RevendedorRepository
from app.schemas.compra import CompraIn, CompraOut


class CompraService:
    def __init__(self, db: Session):
        self.repository = CompraRepository(db)
        self.revendedor_repository = RevendedorRepository(db)

    def create(self, compra: CompraIn) -> CompraOut:
        revendedor_id = self.revendedor_repository.get_revendedor_by_cpf(
            compra.cpf_revendedor
        ).id
        compra_model = self.repository.create(compra, revendedor_id)

        return CompraOut(
            codigo=compra_model.codigo,
            valor=compra_model.valor,
            data=compra_model.data,
            porcentagem_de_cashback=compra_model.porcentagem_de_cashback or "0.10",
            valor_de_cashback="10.00",
            status=compra_model.status,
        )

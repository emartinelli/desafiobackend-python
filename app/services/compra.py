from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.compra import Compra as CompraModel
from app.repositories.compra import CompraRepository
from app.repositories.revendedor import RevendedorRepository
from app.schemas.compra import CompraIn, CompraOut


class CompraService:
    def __init__(self, db: Session):
        self.repository = CompraRepository(db)
        self.revendedor_repository = RevendedorRepository(db)

    def create(self, compra: CompraIn) -> CompraOut:
        revendedor = self.revendedor_repository.get_revendedor_by_cpf(
            compra.cpf_revendedor
        )

        if not revendedor:
            # TODO: create specific exception
            raise Exception(
                f"Revendedor with given cpf `{compra.cpf_revendedor}` does not exist"
            )

        compra_model = self.repository.create(
            compra, revendedor.id, porcentagem_de_cashback=Decimal("0.1")
        )

        return self._map_model_to_schema(compra_model)

    def get_compras(self) -> list[CompraOut]:
        return [
            self._map_model_to_schema(compra_model)
            for compra_model in self.repository.get_all()
        ]

    def _map_model_to_schema(self, compra_model: CompraModel) -> CompraOut:
        return CompraOut(
            codigo=compra_model.codigo,
            valor=compra_model.valor,
            data=compra_model.data,
            porcentagem_de_cashback=compra_model.porcentagem_de_cashback,
            valor_de_cashback=compra_model.valor * compra_model.porcentagem_de_cashback,
            status=compra_model.status,
        )

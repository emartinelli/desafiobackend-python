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
        revendedor = self.revendedor_repository.get_revendedor_by_cpf(
            compra.cpf_revendedor
        )

        if not revendedor:
            # TODO: create specific exception
            raise Exception(
                f"Revendedor with given cpf `{compra.cpf_revendedor}` does not exist"
            )

        compra_model = self.repository.create(compra, revendedor.id)

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
            porcentagem_de_cashback=compra_model.porcentagem_de_cashback or "0.10",
            valor_de_cashback="10.00",
            status=compra_model.status,
        )

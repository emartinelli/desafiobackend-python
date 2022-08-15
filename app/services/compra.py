import logging
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions.revendedor import RevendedorNotFoundException
from app.models.compra import Compra as CompraModel
from app.repositories.cashback import CashbackRepository
from app.repositories.compra import CompraRepository
from app.repositories.revendedor import RevendedorRepository
from app.schemas.compra import CompraIn, CompraOut

logger = logging.getLogger(__name__)


class CompraService:
    def __init__(self, db: Session):
        self.repository = CompraRepository(db)
        self.revendedor_repository = RevendedorRepository(db)
        self.cashback_repository = CashbackRepository(db)

    def create(self, compra: CompraIn) -> CompraOut:
        logger.info(f"Criando compra com codigo: {compra.codigo}")
        revendedor = self.revendedor_repository.get_revendedor_by_cpf(
            compra.cpf_revendedor
        )
        if not revendedor:
            raise RevendedorNotFoundException(
                f"Revendedor with given cpf `{compra.cpf_revendedor}` does not exist"
            )

        compra_model = self.repository.create(
            compra,
            revendedor.id,
            status=revendedor.status_compra_default,
        )
        logger.info(f"Compra com codigo: {compra.codigo} criada")

        return self.map_model_to_schema(compra_model)

    @classmethod
    def map_model_to_schema(
        cls,
        compra_model: CompraModel,
        porcentagem_de_cashback: Optional[Decimal] = None,
        valor_de_cashback: Optional[Decimal] = None,
    ) -> CompraOut:
        compra_out = CompraOut(
            codigo=compra_model.codigo,
            valor=compra_model.valor,
            data=compra_model.data,
            status=compra_model.status,
        )

        if porcentagem_de_cashback and valor_de_cashback:
            compra_out.porcentagem_de_cashback = porcentagem_de_cashback
            compra_out.valor_de_cashback = valor_de_cashback

        return compra_out

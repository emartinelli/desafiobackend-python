from decimal import Decimal
from sqlalchemy.orm import Session

from app.exceptions.revendedor import RevendedorNotFoundException
from app.infra.clients.cashback import CashbackClient
from app.repositories.revendedor import RevendedorRepository
from app.schemas.cashback import CashbackAcumuladoOut
from app.models.cashback import CashbackCriterio
from psycopg2.extras import NumericRange


class CashbackRepository:
    def __init__(self, db: Session) -> None:
        self.client = CashbackClient()
        self.db = db
        self.revendedor_repository = RevendedorRepository(db)

    def get_cashback_acumulado(self, cpf: str) -> CashbackAcumuladoOut:
        revendedor = self.revendedor_repository.get_revendedor_by_cpf(cpf)
        if not revendedor:
            raise RevendedorNotFoundException(
                f"Revendedor with given cpf `{cpf}` does not exist"
            )

        return CashbackAcumuladoOut(
            revendedor=RevendedorRepository.map_model_to_schema(revendedor),
            cashback_acumulado=self.client.get_cashback_acumulado(cpf),
        )

    def create_criterio(
        self, intervalo: NumericRange, porcentagem_de_cashback=Decimal
    ) -> CashbackCriterio:
        cash_back_criterio = CashbackCriterio(
            intervalo=intervalo,
            porcentagem_de_cashback=porcentagem_de_cashback,
        )
        self.db.add(cash_back_criterio)
        self.db.commit()
        self.db.refresh(cash_back_criterio)
        return cash_back_criterio

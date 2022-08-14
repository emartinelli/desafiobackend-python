from sqlalchemy.orm import Session

from app.exceptions.revendedor import RevendedorNotFoundException
from app.infra.clients.cashback import CashbackClient
from app.repositories.revendedor import RevendedorRepository
from app.schemas.cashback import CashbackAcumuladoOut


class CashbackRepository:
    def __init__(self, db: Session) -> None:
        self.client = CashbackClient()
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

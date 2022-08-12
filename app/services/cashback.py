from sqlalchemy.orm import Session

from app.exceptions.revendedor import RevendedorNotFoundException
from app.repositories.cashback import CashbackRepository
from app.repositories.revendedor import RevendedorRepository


class CashbackService:
    def __init__(self, db: Session) -> None:
        self.repository = CashbackRepository()
        self.revendedor_repository = RevendedorRepository(db)

    def get_cashback_acumulado(self, cpf: str) -> float:
        revendedor = self.revendedor_repository.get_revendedor_by_cpf(cpf)
        if not revendedor:
            raise RevendedorNotFoundException(
                f"Revendedor with given cpf `{cpf}` does not exist"
            )

        return self.repository.get_cashback_acumulado(cpf)

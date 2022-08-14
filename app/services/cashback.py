from sqlalchemy.orm import Session

from app.repositories.cashback import CashbackRepository
from app.schemas.cashback import CashbackAcumuladoOut


class CashbackService:
    def __init__(self, db: Session) -> None:
        self.repository = CashbackRepository(db)

    def get_cashback_acumulado(self, cpf: str) -> CashbackAcumuladoOut:
        return self.repository.get_cashback_acumulado(cpf)

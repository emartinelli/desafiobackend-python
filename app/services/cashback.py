from app.repositories.cashback import CashbackRepository


class CashbackService:
    def __init__(self) -> None:
        self.repository = CashbackRepository()

    def get_cashback_acumulado(self, cpf: str) -> float:
        return self.repository.get_cashback_acumulado(cpf)

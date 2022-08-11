from app.infra.clients.cashback import CashbackClient


class CashbackRepository:
    def __init__(self) -> None:
        self.client = CashbackClient()

    def get_cashback_acumulado(self, cpf: str) -> float:
        return self.client.get_cashback_acumulado(cpf)

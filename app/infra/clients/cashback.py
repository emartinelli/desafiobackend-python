import logging
from urllib.parse import urljoin
from app.infra.settings import settings
import requests

cashback_path = "/v1/cashback"

logging.basicConfig(level=logging.DEBUG)


class CashbackClient:
    def get_cashback_acumulado(self, cpf: str) -> float:
        response = requests.get(
            urljoin(settings.CASHBACK_SERVICE_URL, cashback_path), params={"cpf": cpf}
        )
        response.raise_for_status()

        data = response.json()
        body = data["body"]

        status_code = data["statusCode"]
        if status_code != 200:
            # TODO: create specific exception
            raise Exception(body["message"])

        return body["credit"]

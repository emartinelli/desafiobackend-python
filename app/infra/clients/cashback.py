from urllib.parse import urljoin

import requests

from app.exceptions.cashback import CashbackClientException
from app.infra.settings import settings

cashback_path = "/v1/cashback"


class CashbackClient:
    def get_cashback_acumulado(self, cpf: str) -> float:
        response = requests.get(
            urljoin(settings.CASHBACK_SERVICE_URL, cashback_path),
            params={"cpf": cpf},
            headers={"token": settings.CASHBACK_SERVICE_TOKEN},
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise CashbackClientException(e) from e

        data = response.json()
        body = data["body"]

        status_code = data["statusCode"]
        if status_code != 200:
            raise CashbackClientException(body["message"])

        return body["credit"]

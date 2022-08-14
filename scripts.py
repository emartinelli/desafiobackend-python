from decimal import Decimal
from webbrowser import get

import typer

from app.controllers.dependencies import get_db
from app.repositories.api_user import APIUserRepository
from app.repositories.cashback import CashbackRepository
from psycopg2.extras import NumericRange

app = typer.Typer()


@app.command()
def create_api_user(username: str, password: str):
    db = next(get_db())
    repository = APIUserRepository(db)
    repository.create(username=username, password=password)


@app.command()
def create_cashback_criterios():
    db = next(get_db())
    repository = CashbackRepository(db)
    repository.create_criterio(
        NumericRange(Decimal("0"), Decimal("1000")), Decimal("0.1")
    )
    repository.create_criterio(
        NumericRange(Decimal("1000"), Decimal("1500")), Decimal("0.15")
    )
    repository.create_criterio(NumericRange(Decimal("1500")), Decimal("0.2"))


if __name__ == "__main__":
    app()

from webbrowser import get

import typer

from app.controllers.dependencies import get_db
from app.repositories.api_user import APIUserRepository

app = typer.Typer()


@app.command()
def create_api_user(username: str, password: str):
    db = next(get_db())
    repository = APIUserRepository(db)
    repository.create(username=username, password=password)


if __name__ == "__main__":
    app()

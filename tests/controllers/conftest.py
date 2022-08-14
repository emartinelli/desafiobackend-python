from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_db
from app.repositories.api_user import APIUserRepository
from main import app
from tests import utils
from app.infra.settings import settings


@pytest.fixture(scope="function")
def client(db_session) -> Generator[Session, None, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def make_revendedor_headers(client: TestClient):
    def _make(email, password):
        return utils.get_revendedor_authentication_headers(client, email, password)

    return _make


@pytest.fixture
def api_user_headers(client: TestClient, db_session: Session) -> dict[str, str]:
    data = {"username": "some-login", "password": "some-password"}
    APIUserRepository(db_session).create(**data)

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

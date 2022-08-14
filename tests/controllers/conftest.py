import pytest
from fastapi.testclient import TestClient

from app.controllers.dependencies import get_db
from main import app
from tests import utils


@pytest.fixture(scope="function")
def client(db_session):
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

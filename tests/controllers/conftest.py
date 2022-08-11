import pytest
from fastapi.testclient import TestClient

from app.controllers.dependencies import get_db
from main import app


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

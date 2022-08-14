from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infra.settings import settings
from app.models.compra import Compra as CompraModel
from app.models.revendedor import Revendedor as Revendedor
from app.repositories.compra import CompraRepository
from app.repositories.revendedor import RevendedorRepository
from app.schemas.compra import CompraIn
from app.schemas.revendedor import RevendedorIn


def create_revendedor(db: Session, revendedor_in: RevendedorIn) -> Revendedor:
    return RevendedorRepository(db).create(revendedor_in)


def create_revendedor_and_compra(
    db: Session,
    compra_in: CompraIn,
    revendedor_in: RevendedorIn,
) -> CompraModel:
    revendedor = create_revendedor(db, revendedor_in)
    return CompraRepository(db).create(compra_in, revendedor_id=revendedor.id)


def get_revendedor_authentication_headers(
    client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/revendedor/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

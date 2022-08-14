from datetime import timedelta

from sqlalchemy.orm import Session

from app.infra.security import create_access_token
from app.infra.settings import settings
from app.models.revendedor import Revendedor as Revendedor
from app.repositories.revendedor import RevendedorRepository
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.schemas.token import Token


class RevendedorService:
    def __init__(self, db: Session):
        self.repository = RevendedorRepository(db)

    def create(self, revendedor: RevendedorIn) -> RevendedorOut:
        revendedor_model = self.repository.create(revendedor)
        return RevendedorRepository.map_model_to_schema(revendedor_model)

    def get_token(self, email: str, password: str) -> Token:
        revendedor = self.repository.authenticate(email, password)
        if not revendedor:
            return None

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                revendedor.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

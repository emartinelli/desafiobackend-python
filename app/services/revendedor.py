from datetime import timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.revendedor import RevendedorNotFoundException
from app.infra.security import create_access_token
from app.infra.settings import settings
from app.models.revendedor import Revendedor as Revendedor
from app.repositories.revendedor import RevendedorRepository
from app.schemas.compra import CompraOut
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.schemas.token import Token
from app.services.compra import CompraService


class RevendedorService:
    def __init__(self, db: Session):
        self.repository = RevendedorRepository(db)

    def create(self, revendedor: RevendedorIn) -> RevendedorOut:
        revendedor_model = self.repository.create(revendedor)
        return RevendedorRepository.map_model_to_schema(revendedor_model)

    def get(self, id: UUID) -> RevendedorOut:
        revendedor_model = self.repository.get(id)
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

    def get_compras(self, cpf: str) -> list[CompraOut]:
        revendedor = self.repository.get_revendedor_by_cpf(cpf)
        if not revendedor:
            raise RevendedorNotFoundException(
                f"Revendedor with given cpf `{cpf}` does not exist"
            )

        return [
            CompraService.map_model_to_schema(*compra)
            for compra in self.repository.get_compras_with_distributed_cashback_per_month(
                revendedor.id
            )
        ]

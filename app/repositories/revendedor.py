from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.revendedor import DuplicateRevendedorException
from app.infra.security import get_password_hash, verify_password
from app.models.revendedor import Revendedor
from app.schemas.revendedor import RevendedorIn, RevendedorOut


class RevendedorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, revendedor: RevendedorIn) -> Revendedor:
        revendedor_model = Revendedor(
            cpf=revendedor.cpf,
            email=revendedor.email,
            nome_completo=revendedor.nome_completo,
            senha_com_hash=get_password_hash(revendedor.senha),
            status_compra_default=revendedor.status_compra_default,
        )

        self.db.add(revendedor_model)
        try:
            self.db.commit()
        except IntegrityError as e:
            raise DuplicateRevendedorException(
                "Revendedor using same information"
            ) from e

        self.db.refresh(revendedor_model)

        return revendedor_model

    def get(self, id: UUID) -> Revendedor:
        return self.db.query(Revendedor).filter(Revendedor.id == id).first()

    def get_revendedor_by_cpf(self, cpf: str) -> Revendedor:
        return self.db.query(Revendedor).filter(Revendedor.cpf == cpf).first()

    def get_by_email(self, email: str) -> Optional[Revendedor]:
        return self.db.query(Revendedor).filter(Revendedor.email == email).first()

    def authenticate(self, email: str, password: str) -> Optional[Revendedor]:
        revendedor = self.get_by_email(email=email)
        if not revendedor:
            return None
        if not verify_password(password, revendedor.senha_com_hash):
            return None
        return revendedor

    @classmethod
    def map_model_to_schema(cls, model: Revendedor) -> RevendedorOut:
        return RevendedorOut(
            nome_completo=model.nome_completo,
            cpf=model.cpf,
            email=model.email,
        )

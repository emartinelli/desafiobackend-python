from typing import Any, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.revendedor import DuplicateRevendedorException
from app.infra.security import get_password_hash, verify_password
from app.models.cashback import CashbackCriterio
from app.models.compra import Compra
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

    def get(self, id: UUID) -> Optional[Revendedor]:
        return self.db.query(Revendedor).filter(Revendedor.id == id).first()

    def get_revendedor_by_cpf(self, cpf: str) -> Optional[Revendedor]:
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

    def get_compras_with_distributed_cashback_per_month(self, id: UUID) -> list[Any]:
        """Query to get the compras with dilluted cashback per month"""

        # Lê os valores acumualdos de compra agrupados por mês
        cashback_acumulado_mes = (
            self.db.query(
                Revendedor.id.label("revendedor_id"),
                func.date_trunc("month", Compra.data).label("mes"),
                func.sum(Compra.valor).label("valor_acumulado"),
            )
            .join(Compra)
            .group_by(func.date_trunc("month", Compra.data), Revendedor.id)
            .cte()
        )

        # Lê os critérios de cashback de acordo o valor acumulado por mês
        porcentagem_de_cashback_mes = (
            self.db.query(
                cashback_acumulado_mes,
                CashbackCriterio.porcentagem_de_cashback.label(
                    "porcentagem_de_cashback"
                ),
            )
            .select_from(CashbackCriterio)
            .join(
                cashback_acumulado_mes,
                CashbackCriterio.intervalo.contains(
                    cashback_acumulado_mes.c.valor_acumulado
                ),
            )
            .cte()
        )

        # Calcular para cada compra de uma pessoa revendedora o valor do cashback
        result = (
            self.db.query(
                Compra,
                porcentagem_de_cashback_mes.c.porcentagem_de_cashback.label(
                    "porcentagem_de_cashback"
                ),
                (
                    Compra.valor * porcentagem_de_cashback_mes.c.porcentagem_de_cashback
                ).label("valor_de_cashback"),
            )
            .select_from(Compra)
            .join(
                porcentagem_de_cashback_mes,
                func.date_trunc("month", Compra.data)
                == porcentagem_de_cashback_mes.c.mes,
            )
            .filter(Compra.revendedor_id == id)
            .order_by(Compra.data.desc())
            .all()
        )

        return result

    @classmethod
    def map_model_to_schema(cls, model: Revendedor) -> RevendedorOut:
        return RevendedorOut(
            nome_completo=model.nome_completo,
            cpf=model.cpf,
            email=model.email,
        )

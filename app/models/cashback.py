import uuid

from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID, NUMRANGE

from app.infra.database.basemodel import Base


class CashbackCriterio(Base):
    __tablename__ = "cashback_criterios"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    intervalo = Column(NUMRANGE, nullable=False)
    porcentagem_de_cashback = Column(Numeric(asdecimal=True), nullable=False)

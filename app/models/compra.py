import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infra.database.basemodel import Base
from app.schemas.compra import StatusEnum


class Compra(Base):
    __tablename__ = "compras"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    valor = Column(Numeric(asdecimal=True), nullable=False)
    data = Column(DateTime, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.em_validacao, nullable=False)
    revendedor_id = Column(
        UUID(as_uuid=True), ForeignKey("revendedores.id"), nullable=False
    )

    revendedor = relationship("Revendedor", back_populates="compras")

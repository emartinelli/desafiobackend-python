import uuid

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infra.database.basemodel import Base
from app.schemas.compra import StatusEnum


class Revendedor(Base):
    __tablename__ = "revendedores"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    nome_completo = Column(String(255), nullable=False)
    status_compra_default = Column(Enum(StatusEnum), nullable=True)

    senha_com_hash = Column(String(255), nullable=False)

    compras = relationship("Compra", back_populates="revendedor")

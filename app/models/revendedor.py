import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infra.database.basemodel import Base


class Revendedor(Base):
    __tablename__ = "revendedores"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    cpf = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    nome_completo = Column(String)
    senha_com_hash = Column(String)

    compras = relationship("Compra", back_populates="revendedor")

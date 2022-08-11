import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infra.database.basemodel import Base


class Compra(Base):
    __tablename__ = "compras"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    codigo = Column(String, unique=True, index=True)
    valor = Column(String)
    data = Column(String)
    status = Column(String, default="Em validação")
    porcentagem_de_cashback = Column(String)
    revendedor_id = Column(UUID(as_uuid=True), ForeignKey("revendedores.id"))

    revendedor = relationship("Revendedor", back_populates="compras")

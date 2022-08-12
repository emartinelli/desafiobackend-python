import enum
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class StatusEnum(str, enum.Enum):
    em_validacao = "Em validação"
    aprovado = "Aprovado"


class CompraIn(BaseModel):
    codigo: str
    valor: Decimal
    data: datetime
    cpf_revendedor: str


class CompraOut(BaseModel):
    codigo: str
    valor: Decimal
    data: datetime
    porcentagem_de_cashback: Decimal
    valor_de_cashback: Decimal
    status: StatusEnum


class Compra(BaseModel):
    codigo: str
    valor: Decimal
    data: datetime
    cpf_do_revendedor: str
    porcentagem_de_cashback: Decimal
    valor_de_cashback: Decimal
    status: StatusEnum

    class Config:
        orm_mode = True

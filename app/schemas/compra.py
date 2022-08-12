from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class StatusEnum(str, Enum):
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

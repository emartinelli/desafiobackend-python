import enum
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, validator


class StatusEnum(str, enum.Enum):
    em_validacao = "Em validação"
    aprovado = "Aprovado"


class CompraIn(BaseModel):
    codigo: str
    valor: Decimal
    data: datetime
    cpf_revendedor: str

    @validator("cpf_revendedor")
    def validate_cpf(cls, v):
        if len(v) != 11:
            raise ValueError("CPF deve conter 11 dígitos")

        return v


class CompraOut(BaseModel):
    codigo: str
    valor: Decimal
    data: datetime
    porcentagem_de_cashback: Decimal
    valor_de_cashback: Decimal
    status: StatusEnum

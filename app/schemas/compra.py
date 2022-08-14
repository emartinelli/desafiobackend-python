import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional

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
    def validate_cpf(cls, v: str) -> str:
        if len(v) != 11:
            raise ValueError("CPF deve conter 11 dígitos")

        return v


class CompraOut(BaseModel):
    codigo: str
    valor: Decimal
    data: datetime
    porcentagem_de_cashback: Optional[Decimal]
    valor_de_cashback: Optional[Decimal]
    status: StatusEnum

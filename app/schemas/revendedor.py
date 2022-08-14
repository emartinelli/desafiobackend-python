from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from app.schemas.compra import StatusEnum


class RevendedorIn(BaseModel):
    nome_completo: str
    cpf: str
    email: EmailStr
    senha: str
    status_compra_default: Optional[StatusEnum] = None

    @validator("cpf")
    def validate_cpf(cls, v):
        if len(v) != 11:
            raise ValueError("CPF deve conter 11 dígitos")

        return v


class RevendedorOut(BaseModel):
    nome_completo: str
    cpf: str
    email: EmailStr

from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class RevendedorIn(BaseModel):
    nome_completo: str
    cpf: str
    email: EmailStr
    senha: str
    status_compra_default: Optional[str] = None

    @validator("cpf")
    def validate_cpf(cls, v):
        if len(v) != 11:
            raise ValueError("CPF deve conter 11 dígitos")

        return v


class RevendedorOut(BaseModel):
    nome_completo: str
    cpf: str
    email: EmailStr

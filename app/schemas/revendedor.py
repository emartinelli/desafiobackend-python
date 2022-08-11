from pydantic import BaseModel


class RevendedorIn(BaseModel):
    nome_completo: str
    cpf: str
    email: str
    senha: str


class RevendedorOut(BaseModel):
    nome_completo: str
    cpf: str
    email: str

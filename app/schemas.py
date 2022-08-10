from pydantic import BaseModel


class RevendedorIn(BaseModel):
    nome_completo: str
    cpf: str
    email: str
    senha: str


class CompraIn(BaseModel):
    codigo: str
    valor: str
    data: str
    cpf_revendedor: str


class CompraOut(BaseModel):
    codigo: str
    valor: str
    data: str
    porcentagem_de_cashback: str
    valor_de_cashback: str
    status: str


class CashbackAcumulado(BaseModel):
    cashback_acumulado: str

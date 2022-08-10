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


class Compra(BaseModel):
    codigo: str
    valor: str
    data: str
    cpf_do_revendedor: str
    porcentagem_de_cashback: str
    valor_de_cashback: str
    status: str

    class Config:
        orm_mode = True


class CashbackAcumulado(BaseModel):
    cashback_acumulado: str

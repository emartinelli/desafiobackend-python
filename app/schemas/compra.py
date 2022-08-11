from pydantic import BaseModel


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

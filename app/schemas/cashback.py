from decimal import Decimal

from pydantic import BaseModel

from app.schemas.revendedor import RevendedorOut


class CashbackAcumuladoOut(BaseModel):
    revendedor: RevendedorOut
    cashback_acumulado: Decimal

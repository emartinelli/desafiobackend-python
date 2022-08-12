from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_db
from ..schemas.cashback import CashbackAcumuladoOut
from ..exceptions.cashback import CashbackClientException
from app.exceptions.revendedor import (
    DuplicateRevendedorException,
    RevendedorNotFoundException,
)
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.services.cashback import CashbackService
from app.services.revendedor import RevendedorService

router = APIRouter()


@router.post("/", response_model=RevendedorOut, status_code=201)
def create_revendedor(revendedor_in: RevendedorIn, db: Session = Depends(get_db)):
    service = RevendedorService(db)
    try:
        return service.create(revendedor_in)
    except DuplicateRevendedorException:
        raise HTTPException(status_code=422, detail="Revendedor já cadastrado")


@router.get("/{cpf}/cashback", response_model=CashbackAcumuladoOut, status_code=200)
def get_cashback_acumulado(cpf: str, db: Session = Depends(get_db)):
    service = CashbackService(db)
    try:
        return service.get_cashback_acumulado(cpf)
    except RevendedorNotFoundException:
        raise HTTPException(status_code=422, detail="Revendedor não encontrado")
    except CashbackClientException as e:
        if 400 <= e.status_code < 500:
            raise HTTPException(status_code=400, detail=e.message)
        else:
            raise HTTPException(status_code=e.status_code, detail=e.message)

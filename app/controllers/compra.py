from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_db
from app.exceptions.compra import DuplicateCompraException
from app.schemas.compra import CompraIn, CompraOut
from app.services.compra import CompraService

router = APIRouter()


@router.post("/", response_model=CompraOut, status_code=201)
def create_compra(compra_in: CompraIn, db: Session = Depends(get_db)):
    service = CompraService(db)
    try:
        return service.create(compra_in)
    except DuplicateCompraException:
        raise HTTPException(status_code=422, detail="Compra já cadastrada")

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_current_api_user, get_db
from app.exceptions.compra import DuplicateCompraException
from app.schemas.compra import CompraIn, CompraOut
from app.services.compra import CompraService, RevendedorNotFoundException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=CompraOut, status_code=201)
def create_compra(
    compra_in: CompraIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_api_user),
):
    service = CompraService(db)
    try:
        return service.create(compra_in)
    except (DuplicateCompraException):
        logger.exception(f"Compra duplicada com codigo: {compra_in.codigo}")
        raise HTTPException(status_code=422, detail="Compra já cadastrada")
    except (RevendedorNotFoundException):
        logger.exception(
            f"Revendedor não econtrada na compra com codigo: {compra_in.codigo}"
        )
        raise HTTPException(
            status_code=422,
            detail=f"Nenhum revendedor encontrado com o CPF `{compra_in.cpf_revendedor}`",
        )

import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session

from app.controllers.dependencies import (get_current_api_user,
                                          get_current_revendedor, get_db)
from app.exceptions.cashback import CashbackClientException
from app.exceptions.revendedor import (DuplicateRevendedorException,
                                       RevendedorNotFoundException)
from app.schemas.cashback import CashbackAcumuladoOut
from app.schemas.compra import CompraOut
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.schemas.token import Token
from app.services.cashback import CashbackService
from app.services.revendedor import RevendedorService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=RevendedorOut, status_code=201)
def create_revendedor(
    revendedor_in: RevendedorIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_api_user),
):
    service = RevendedorService(db)
    try:
        return service.create(revendedor_in)
    except DuplicateRevendedorException:
        logger.exception(f"Revendedor duplicado com cpf: {revendedor_in.cpf}")
        raise HTTPException(status_code=422, detail="Revendedor já cadastrado")


@router.get("/{cpf}/cashback", response_model=CashbackAcumuladoOut, status_code=200)
def get_cashback_acumulado(
    cpf: str, db: Session = Depends(get_db), current_user=Depends(get_current_api_user)
):
    service = CashbackService(db)
    try:
        return service.get_cashback_acumulado(cpf)
    except RevendedorNotFoundException:
        logger.exception(f"Revendedor não encontrado com cpf: {cpf}")
        raise HTTPException(status_code=422, detail="Revendedor não encontrado")
    except CashbackClientException as e:
        if 400 <= e.status_code < 500:
            raise HTTPException(status_code=400, detail=e.message)
        else:
            raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    service = RevendedorService(db)
    token = service.get_token(email=form_data.username, password=form_data.password)
    if not token:
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")

    return token


@router.get("/login/validate", response_model=RevendedorOut)
def login_validate(current_revendedor: RevendedorOut = Depends(get_current_revendedor)):
    return current_revendedor


@router.get("/{cpf}/compras", response_model=Page[CompraOut])
def get_compras_with_cashback(
    cpf: str, db: Session = Depends(get_db), current_user=Depends(get_current_api_user)
):
    service = RevendedorService(db)
    try:
        return paginate(service.get_compras(cpf))
    except RevendedorNotFoundException:
        logger.exception(f"Revendedor não encontrado com cpf: {cpf}")
        raise HTTPException(status_code=422, detail="Revendedor não encontrado")


add_pagination(router)

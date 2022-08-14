from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controllers.dependencies import (
    get_current_revendedor,
    get_db,
    get_current_api_user,
)
from app.exceptions.cashback import CashbackClientException
from app.exceptions.revendedor import (
    DuplicateRevendedorException,
    RevendedorNotFoundException,
)
from app.schemas.cashback import CashbackAcumuladoOut
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.schemas.token import Token
from app.services.cashback import CashbackService
from app.services.revendedor import RevendedorService

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
        raise HTTPException(status_code=422, detail="Revendedor já cadastrado")


@router.get("/{cpf}/cashback", response_model=CashbackAcumuladoOut, status_code=200)
def get_cashback_acumulado(
    cpf: str, db: Session = Depends(get_db), current_user=Depends(get_current_api_user)
):
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

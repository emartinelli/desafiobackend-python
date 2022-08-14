from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_db
from app.infra.security import create_access_token
from app.infra.settings import settings
from app.repositories.api_user import APIUserRepository
from app.schemas.token import Token

router = APIRouter()


@router.post("/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    repository = APIUserRepository(db)
    user = repository.authenticate(
        username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

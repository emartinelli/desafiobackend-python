from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.infra import security
from app.infra.database.session import SessionLocal
from app.infra.settings import settings
from app.models.revendedor import Revendedor
from app.repositories.api_user import APIUserRepository
from app.schemas.token import TokenPayload
from app.services.revendedor import RevendedorService

api_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token", scheme_name="api"
)
revendedor_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/revendedor/login/access-token",
    scheme_name="revendedor",
)


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_revendedor(
    db: Session = Depends(get_db), token: str = Depends(revendedor_oauth2)
) -> Revendedor:
    token_data = decode_token(token)

    service = RevendedorService(db)
    revendedor = service.get(id=token_data.sub)
    if not revendedor:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return revendedor


def get_current_api_user(
    db: Session = Depends(get_db), token: str = Depends(api_oauth2)
):
    token_data = decode_token(token)

    repository = APIUserRepository(db)
    user = repository.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="API user not found")
    return user


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        e
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data

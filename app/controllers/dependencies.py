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
from app.repositories.revendedor import RevendedorRepository
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/revendedor/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_revendedor(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Revendedor:
    revendedor_repository = RevendedorRepository(db)

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = revendedor_repository.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return user

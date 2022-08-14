from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.infra.security import get_password_hash, verify_password
from app.models.api_user import APIUser


class APIUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username, password) -> APIUser:
        api_user = APIUser(
            username=username,
            hashed_password=get_password_hash(password),
        )
        self.db.add(api_user)
        self.db.commit()
        self.db.refresh(api_user)

        return api_user

    def get(self, id: UUID) -> Optional[APIUser]:
        return self.db.query(APIUser).filter(APIUser.id == id).first()

    def get_by_username(self, username: str) -> Optional[APIUser]:
        return self.db.query(APIUser).filter(APIUser.username == username).first()

    def authenticate(self, username: str, password: str) -> Optional[APIUser]:
        user = self.get_by_username(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

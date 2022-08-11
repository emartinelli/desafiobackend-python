from email.generator import Generator

from sqlalchemy.orm import Session

from app.infra.database.session import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

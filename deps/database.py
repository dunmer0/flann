from typing import Generator, Any, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db.db import SessionLocal


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    # except Exception:
    #     db.rollback()
    #     raise
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
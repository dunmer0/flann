from typing import Annotated, Generator, Any

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

os.makedirs("database", exist_ok=True)

DATABASE_URL = "sqlite:///database/flann.db"

engine = create_engine(DATABASE_URL, echo="debug")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)




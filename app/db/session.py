from __future__ import annotations

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
import os
import pathlib


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


def init_engine_and_create(database_url: str) -> None:
    global engine, SessionLocal
    if database_url.startswith("sqlite"):
        # ensure data directory exists
        pathlib.Path("data").mkdir(exist_ok=True)
        engine = create_engine(database_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
    from app.db.models import Resume, Assessment  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



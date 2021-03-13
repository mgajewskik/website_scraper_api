from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.settings import POSTGRES_URL
from . import models
from app.utils import log


engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, Session, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_db():

    models.Base.metadata.create_all(bind=engine)
    log.debug("All tables created. Database ready.")

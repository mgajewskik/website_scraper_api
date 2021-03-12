import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# pg = {
    # "host": os.getenv("PG_HOST"),
    # "db": os.getenv("PG_DATABASE"),
    # "user": os.getenv("PG_USER"),
    # "password": os.getenv("PG_PASSWORD"),
    # "port": os.getenv("PG_PORT"),
# }

pg = {
    "host": "localhost",
    "db": "postgres",
    "user": "postgres",
    "password": "lytbryt234",
    "port": 5433,
}

POSTGRES_URL = f"postgresql://{pg['user']}:{pg['password']}@{pg['host']}:{pg['port']}/{pg['db']}"

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

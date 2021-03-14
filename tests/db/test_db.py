from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PG = {
    "host": "localhost",
    "db": "postgres",
    "user": "postgres",
    "password": "password_test",
    "port": 5441,
}


TEST_POSTGRES_URL = (
    f"postgresql://{PG['user']}:{PG['password']}@{PG['host']}:{PG['port']}/{PG['db']}"
)


engine = create_engine(TEST_POSTGRES_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

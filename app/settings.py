import os

DATA_PATH = os.getenv("DATA_PATH")

PG = {
    "host": os.getenv("POSTGRES_NAME"),
    "db": os.getenv("PG_DATABASE"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "port": os.getenv("PG_PORT"),
}


POSTGRES_URL = (
    f"postgresql://{PG['user']}:{PG['password']}@{PG['host']}:{PG['port']}/{PG['db']}"
)

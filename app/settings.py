import os


# PG = {
# "host": os.getenv("PG_HOST"),
# "db": os.getenv("PG_DATABASE"),
# "user": os.getenv("PG_USER"),
# "password": os.getenv("PG_PASSWORD"),
# "port": os.getenv("PG_PORT"),
# }

PG = {
    "host": "localhost",
    "db": "postgres",
    "user": "postgres",
    "password": "lytbryt234",
    "port": 5433,
}


POSTGRES_URL = (
    f"postgresql://{PG['user']}:{PG['password']}@{PG['host']}:{PG['port']}/{PG['db']}"
)

DATA_PATH = "data"

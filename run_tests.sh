docker-compose -f tests/db/test_postgres.yml down -t0
docker-compose -f tests/db/test_postgres.yml up -d

export DATA_PATH="tests/test_data"
export POSTGRES_NAME=localhost
export PG_DATABASE=postgres
export PG_USER=postgres
export PG_PASSWORD=password_test
export PG_PORT=5441

poetry run pytest --cov=app tests/ -vv

docker-compose -f tests/db/test_postgres.yml down -t0

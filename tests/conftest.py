import os
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.database import get_db
from app.db import models
from app.main import app
from tests.db.test_db import override_get_db, engine, TestingSessionLocal


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db() -> Generator:
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_data_path() -> str:

    return str(Path(__file__).parent.joinpath("test_data"))


@pytest.fixture
def test_file(test_data_path) -> str:

    with open(os.path.join(test_data_path, "jsonapi.html"), "r") as file:
        return file.read()


@pytest.fixture
def parsed_test_file(test_data_path) -> str:

    with open(os.path.join(test_data_path, "parsed_text.txt"), "r") as file:
        return file.read().strip()


@pytest.fixture
def cleanup(test_data_path):

    yield

    os.remove(os.path.join(test_data_path, "1.zip"))


@pytest.fixture(scope="session")
def data_path():

    os.environ["DATA_PATH"] = "tests/test_data"

import os
from pathlib import Path

import pytest


@pytest.fixture
def get_test_data_path():

    return str(Path(__file__).parent.joinpath("test_data"))


@pytest.fixture
def get_test_file(get_test_data_path):

    with open(os.path.join(get_test_data_path, "jsonapi.html"), "r") as file:
        return file.read()


@pytest.fixture
def get_parsed_test_file(get_test_data_path):

    with open(os.path.join(get_test_data_path, "parsed_text.txt"), "r") as file:
        return file.read().strip()


@pytest.fixture
def cleanup(get_test_data_path):

    yield

    os.remove(os.path.join(get_test_data_path, "1.zip"))

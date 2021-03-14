import types

from app.db.database import get_db


def test_get_db_instance():

    assert isinstance(get_db(), types.GeneratorType)

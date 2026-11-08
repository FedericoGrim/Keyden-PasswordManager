import importlib
import os

import pytest


@pytest.fixture(autouse=True)
def db_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key, value in {
        "DB_USER": "u",
        "DB_PASSWORD": "p",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "d",
    }.items():
        monkeypatch.setenv(key, value)


def test_engine_uses_the_installed_psycopg2_driver() -> None:
    from infrastructure.databases import database

    database = importlib.reload(database)

    assert database.engine.dialect.driver == "psycopg2"
    assert os.getenv("DB_NAME") == "d"

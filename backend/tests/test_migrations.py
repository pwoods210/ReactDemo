import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text


@pytest.fixture
def migrated_database():
    database_url = os.environ.get("TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("TEST_DATABASE_URL is required for migration tests")

    engine = create_engine(database_url)

    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))

    alembic_config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    command.upgrade(alembic_config, "head")

    try:
        yield engine
    finally:
        with engine.begin() as connection:
            connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
            connection.execute(text("CREATE SCHEMA public"))

        engine.dispose()


@pytest.mark.integration
def test_alembic_upgrade_creates_expected_discovery_schema(
    migrated_database,
):
    inspector = inspect(migrated_database)
    columns = {
        column["name"]
        for column in inspector.get_columns("discoveries")
    }
    indexes = {
        index["name"]: index
        for index in inspector.get_indexes("discoveries")
    }

    assert "discoveries" in inspector.get_table_names()
    assert columns == {
        "id",
        "token_address",
        "pair_address",
        "name",
        "symbol",
        "source",
        "exchange",
        "token_profile",
        "pairs_data",
        "status",
        "discovered_at",
        "graduated_at",
        "dismissed_at",
    }
    assert indexes["ix_discoveries_token_address"]["unique"] is True
    assert indexes["ix_discoveries_pair_address"]["unique"] is False

    with migrated_database.connect() as connection:
        revision = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()

    assert revision == "ccf8ecc64082"

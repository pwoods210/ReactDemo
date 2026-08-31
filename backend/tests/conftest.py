import os


# Tests should never depend on a developer's local or production database URL.
# An integration run may explicitly provide TEST_DATABASE_URL instead.
test_database_url = os.environ.get("TEST_DATABASE_URL")

if test_database_url:
    database_name = test_database_url.rsplit("/", 1)[-1].split("?", 1)[0]

    if not database_name.endswith("_test"):
        raise RuntimeError(
            "TEST_DATABASE_URL must point to a database whose name ends in "
            "'_test'"
        )

os.environ["DATABASE_URL"] = test_database_url or "sqlite+pysqlite:///:memory:"

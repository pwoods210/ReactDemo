import os


# Tests should never depend on a developer's local or production database URL.
# An integration run may explicitly provide TEST_DATABASE_URL instead.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "sqlite+pysqlite:///:memory:",
)

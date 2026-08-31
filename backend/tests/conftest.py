import os


# Tests should never depend on a developer's local or production database URL.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

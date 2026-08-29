import os
from pathlib import Path

import pytest

os.environ.setdefault("BBI_DATABASE_URL", "sqlite+aiosqlite:///./var/test-bbi.sqlite3")


@pytest.fixture
def root() -> Path:
    return Path(__file__).resolve().parents[2]

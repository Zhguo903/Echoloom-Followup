"""Validate the synthetic corpus and initialize local SQLite tables."""

import asyncio

from bbi.config import get_settings
from bbi.evaluation.scenarios import lint_scenarios
from bbi.prompts.loader import repo_root
from bbi.storage.db import Database


async def main() -> None:
    errors = lint_scenarios([repo_root() / "data" / "scenarios"])
    if errors:
        raise SystemExit("\n".join(errors))
    database = Database(get_settings().database_url)
    await database.create_all()
    await database.dispose()
    print("validated 24 synthetic scenarios and initialized the local database")


if __name__ == "__main__":
    asyncio.run(main())

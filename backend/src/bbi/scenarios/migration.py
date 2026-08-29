import json
from pathlib import Path
from typing import Any

import yaml

from bbi.domain.scenarios import Scenario


def load_raw_scenario(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"scenario root must be an object: {path}")
    return value


def migrate_raw_scenario(raw: dict[str, Any]) -> dict[str, Any]:
    """Return canonical v2 data; v1 conversion happens only in memory."""

    return Scenario.model_validate(raw).model_dump(mode="json")


def migrate_scenario_file(source: Path, destination: Path, *, overwrite: bool = False) -> Path:
    if destination.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite scenario: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    migrated = migrate_raw_scenario(load_raw_scenario(source))
    destination.write_text(
        json.dumps(migrated, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return destination

import hashlib
import os
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(
    root: Path, config: dict[str, Any], scenario_files: list[Path], prompt_hashes: dict[str, str]
) -> dict[str, Any]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
        )
    except subprocess.CalledProcessError:
        commit, dirty = None, True
    lockfiles = [path for path in [root / "uv.lock", root / "pnpm-lock.yaml"] if path.exists()]
    return {
        "campaign_id": config["campaign_id"],
        "repository_commit": commit,
        "dirty_working_tree": dirty,
        "python_version": platform.python_version(),
        "node_version": _command_version(["node", "--version"]),
        "lockfile_hashes": {path.name: _hash(path) for path in lockfiles},
        "scenario_hashes": {str(path.relative_to(root)): _hash(path) for path in scenario_files},
        "prompt_hashes": prompt_hashes,
        "config_hash": hashlib.sha256(
            __import__("json").dumps(config, sort_keys=True).encode()
        ).hexdigest(),
        "provider": config["provider"],
        "seeds": {"run": config["run"]["seed"]},
        "started_at": datetime.now(UTC).isoformat(),
        "environment": {
            "BBI_DEFAULT_PROVIDER": os.getenv("BBI_DEFAULT_PROVIDER", "mock"),
            "BBI_STUDY_MODE": os.getenv("BBI_STUDY_MODE", "false"),
            "secret_values": "REDACTED",
        },
        "failed_runs": [],
        "excluded_runs": [],
    }


def _command_version(command: list[str]) -> str | None:
    try:
        return subprocess.run(command, text=True, capture_output=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None

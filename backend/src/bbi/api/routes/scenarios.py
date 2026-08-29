from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from bbi.api.dependencies import require_admin
from bbi.domain.scenarios import Scenario
from bbi.evaluation.scenarios import discover_scenarios, lint_scenarios
from bbi.prompts.loader import repo_root

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


def all_scenarios() -> list[Scenario]:
    return discover_scenarios(
        [repo_root() / "data" / "scenarios" / "golden", repo_root() / "data" / "scenarios" / "core"]
    )


@router.get("")
async def list_scenarios() -> list[Scenario]:
    return all_scenarios()


@router.get("/{scenario_id}")
async def get_scenario(scenario_id: str) -> Scenario:
    for scenario in all_scenarios():
        if scenario.scenario_id == scenario_id:
            return scenario
    raise HTTPException(
        status_code=404,
        detail={"code": "scenario_not_found", "message": "Synthetic scenario not found."},
    )


@router.post("/validate", dependencies=[Depends(require_admin)])
async def validate_scenarios() -> dict[str, object]:
    root = repo_root() / "data" / "scenarios"
    errors = lint_scenarios([Path(root)])
    return {"valid": not errors, "errors": errors}

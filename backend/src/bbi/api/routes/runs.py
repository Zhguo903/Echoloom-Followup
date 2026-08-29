from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from bbi.api.dependencies import DbSession
from bbi.api.routes.scenarios import all_scenarios
from bbi.domain.enums import MethodName
from bbi.domain.runs import RunRecord
from bbi.domain.scenarios import Scenario
from bbi.pipeline.reconsider_lite import PipelineOptions, run_method
from bbi.providers.mock import RuleBasedMockProvider
from bbi.storage.repositories import RunRepository

router = APIRouter(prefix="/api", tags=["runs"])


class RunRequest(BaseModel):
    scenario_id: str | None = None
    scenario: Scenario | None = None
    method: MethodName = MethodName.RECONSIDER_LITE
    provider: Literal["mock"] = "mock"
    seed: int = 454491


class CompareRequest(BaseModel):
    scenario_id: str
    provider: Literal["mock"] = "mock"
    seed: int = 454491


def resolve_scenario(scenario_id: str | None, inline: Scenario | None = None) -> Scenario:
    if inline:
        return inline
    for scenario in all_scenarios():
        if scenario.scenario_id == scenario_id:
            return scenario
    raise HTTPException(
        status_code=404,
        detail={"code": "scenario_not_found", "message": "Synthetic scenario not found."},
    )


@router.post("/runs", response_model=RunRecord)
async def create_run(request: RunRequest, db: DbSession) -> RunRecord:
    scenario = resolve_scenario(request.scenario_id, request.scenario)
    record = await run_method(
        scenario, request.method, RuleBasedMockProvider(), PipelineOptions(seed=request.seed)
    )
    await RunRepository(db).add(record)
    return record


@router.get("/runs/{run_id}", response_model=RunRecord)
async def get_run(run_id: str, db: DbSession) -> RunRecord:
    record = await RunRepository(db).get(run_id)
    if not record:
        raise HTTPException(
            status_code=404, detail={"code": "run_not_found", "message": "Run not found."}
        )
    return record


@router.get("/runs", response_model=list[RunRecord])
async def list_runs(
    db: DbSession, scenario_id: str | None = None, method: str | None = None
) -> list[RunRecord]:
    return await RunRepository(db).list(scenario_id, method)


@router.post("/compare", response_model=list[RunRecord])
async def compare(request: CompareRequest, db: DbSession) -> list[RunRecord]:
    scenario = resolve_scenario(request.scenario_id)
    records = []
    for method in MethodName:
        record = await run_method(
            scenario, method, RuleBasedMockProvider(), PipelineOptions(seed=request.seed)
        )
        await RunRepository(db).add(record)
        records.append(record)
    return records

import csv
import io
import json

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy import delete, select

from bbi.api.dependencies import DbSession, require_admin
from bbi.storage.models import StudyAssignmentRow, StudyResponseRow, StudySessionRow
from bbi.storage.repositories import RunRepository

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/export/runs")
async def export_runs(db: DbSession) -> PlainTextResponse:
    records = await RunRepository(db).list()
    return PlainTextResponse(
        "\n".join(
            json.dumps(record.model_dump(mode="json"), ensure_ascii=False) for record in records
        ),
        media_type="application/x-ndjson",
    )


@router.get("/export/study")
async def export_study(db: DbSession) -> PlainTextResponse:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["participant_code", "assignment_id", "ratings", "rationale", "skipped"])
    rows = (
        await db.execute(
            select(StudySessionRow, StudyAssignmentRow, StudyResponseRow)
            .join(
                StudyAssignmentRow,
                StudyAssignmentRow.session_id == StudySessionRow.session_id,
            )
            .join(
                StudyResponseRow,
                StudyResponseRow.assignment_id == StudyAssignmentRow.assignment_id,
            )
        )
    ).all()
    for study_session, assignment, response in rows:
        writer.writerow(
            [
                study_session.participant_code,
                assignment.assignment_id,
                json.dumps(response.ratings),
                response.rationale,
                response.skipped,
            ]
        )
    return PlainTextResponse(output.getvalue(), media_type="text/csv")


@router.post("/reset-demo-data")
async def reset_demo_data(db: DbSession) -> dict[str, bool]:
    await RunRepository(db).clear()
    await db.execute(delete(StudyResponseRow))
    await db.execute(delete(StudyAssignmentRow))
    await db.execute(delete(StudySessionRow))
    await db.commit()
    return {"reset": True}

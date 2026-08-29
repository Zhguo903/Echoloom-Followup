import random
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select

from bbi.api.dependencies import DbSession, require_study
from bbi.domain.study import StudyRating, StudySession, StudySessionCreate
from bbi.storage.models import StudyAssignmentRow, StudyResponseRow, StudySessionRow

router = APIRouter(prefix="/api/study", tags=["study"], dependencies=[Depends(require_study)])


@router.post("/sessions", response_model=StudySession)
async def create_session(payload: StudySessionCreate, db: DbSession) -> StudySession:
    if not payload.adult_eligible or not payload.consented:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "consent_required",
                "message": "Adult eligibility and consent are required.",
            },
        )
    seed = random.SystemRandom().randint(1, 2**31 - 1)
    session = StudySession(
        session_id=f"study_{uuid.uuid4().hex[:16]}",
        participant_code=f"P-{uuid.uuid4().hex[:8].upper()}",
        protocol_version=payload.protocol_version,
        consented_at=datetime.now(UTC),
        assignment_seed=seed,
    )
    db.add(
        StudySessionRow(
            session_id=session.session_id,
            participant_code=session.participant_code,
            protocol_version=session.protocol_version,
            consent_status=True,
            consented_at=session.consented_at,
            assignment_seed=seed,
            status="active",
            withdrawal_at=None,
        )
    )
    await db.commit()
    return session


@router.get("/sessions/{session_id}/next")
async def next_assignment(session_id: str, db: DbSession) -> dict[str, object]:
    session = await db.get(StudySessionRow, session_id)
    if not session or session.status != "active":
        raise HTTPException(
            status_code=404,
            detail={
                "code": "session_not_found",
                "message": "Active study session not found.",
            },
        )
    assignment_id = f"assignment_{session_id}"
    assignment = await db.get(StudyAssignmentRow, assignment_id)
    if assignment is None:
        assignment = StudyAssignmentRow(
            assignment_id=assignment_id,
            session_id=session_id,
            scenario_id="blinded_synthetic_scenario",
            blinded_response_ids=["A"],
            display_order=["A"],
            completion_status="pending",
        )
        db.add(assignment)
        await db.commit()
    return {
        "assignment_id": assignment_id,
        "scenario": "blinded_synthetic_scenario",
        "responses": [{"response_id": "A", "text": "A blinded synthetic response."}],
        "method_labels_hidden": True,
    }


@router.post("/sessions/{session_id}/responses")
async def add_response(session_id: str, payload: StudyRating, db: DbSession) -> dict[str, bool]:
    session = await db.get(StudySessionRow, session_id)
    assignment = await db.get(StudyAssignmentRow, payload.assignment_id)
    if not session or session.status != "active" or not assignment:
        raise HTTPException(
            status_code=404,
            detail={"code": "session_not_found", "message": "Study session not found."},
        )
    ratings = payload.model_dump(exclude={"assignment_id", "rationale", "skipped"})
    db.add(
        StudyResponseRow(
            response_id=f"response_{uuid.uuid4().hex[:16]}",
            assignment_id=payload.assignment_id,
            ratings=ratings,
            rationale=payload.rationale,
            skipped=payload.skipped,
            created_at=datetime.now(UTC),
        )
    )
    assignment.completion_status = "complete"
    await db.commit()
    return {"saved": True}


@router.post("/sessions/{session_id}/withdraw")
async def withdraw(session_id: str, db: DbSession) -> dict[str, bool]:
    session = await db.get(StudySessionRow, session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail={"code": "session_not_found", "message": "Study session not found."},
        )
    assignment_ids = list(
        await db.scalars(
            select(StudyAssignmentRow.assignment_id).where(
                StudyAssignmentRow.session_id == session_id
            )
        )
    )
    if assignment_ids:
        await db.execute(
            delete(StudyResponseRow).where(StudyResponseRow.assignment_id.in_(assignment_ids))
        )
    session.status = "withdrawn"
    session.withdrawal_at = datetime.now(UTC)
    await db.commit()
    return {"withdrawn": True, "responses_deleted": True}

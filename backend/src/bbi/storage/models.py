from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RunRow(Base):
    __tablename__ = "runs"
    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    campaign_id: Mapped[str] = mapped_column(String(128), index=True)
    scenario_id: Mapped[str] = mapped_column(String(160), index=True)
    scenario_version: Mapped[int] = mapped_column(Integer)
    method: Mapped[str] = mapped_column(String(64), index=True)
    provider: Mapped[str] = mapped_column(String(64))
    model: Mapped[str] = mapped_column(String(128))
    prompt_hashes: Mapped[dict[str, str]] = mapped_column(JSON)
    config_hash: Mapped[str] = mapped_column(String(64))
    structured_result: Mapped[dict[str, Any]] = mapped_column(JSON)
    visible_reply: Mapped[str] = mapped_column(Text)
    validation_status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class StudySessionRow(Base):
    __tablename__ = "study_sessions"
    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    participant_code: Mapped[str] = mapped_column(String(64), unique=True)
    protocol_version: Mapped[str] = mapped_column(String(64))
    consent_status: Mapped[bool] = mapped_column(Boolean)
    consented_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    assignment_seed: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32))
    withdrawal_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class StudyAssignmentRow(Base):
    __tablename__ = "study_assignments"
    assignment_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        ForeignKey("study_sessions.session_id", ondelete="CASCADE"), index=True
    )
    scenario_id: Mapped[str] = mapped_column(String(160))
    blinded_response_ids: Mapped[list[str]] = mapped_column(JSON)
    display_order: Mapped[list[str]] = mapped_column(JSON)
    completion_status: Mapped[str] = mapped_column(String(32), default="pending")


class StudyResponseRow(Base):
    __tablename__ = "study_responses"
    response_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assignment_id: Mapped[str] = mapped_column(
        ForeignKey("study_assignments.assignment_id", ondelete="CASCADE"), index=True
    )
    ratings: Mapped[dict[str, Any]] = mapped_column(JSON)
    rationale: Mapped[str] = mapped_column(Text, default="")
    skipped: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

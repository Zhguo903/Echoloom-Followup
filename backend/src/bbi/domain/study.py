from datetime import datetime

from pydantic import BaseModel, Field


class StudySessionCreate(BaseModel):
    adult_eligible: bool
    consented: bool
    protocol_version: str


class StudyRating(BaseModel):
    assignment_id: str
    relational_appropriateness: int = Field(ge=1, le=7)
    helpfulness: int = Field(ge=1, le=7)
    naturalness: int = Field(ge=1, le=7)
    continuity: int = Field(ge=1, le=7)
    feeling_understood: int = Field(ge=1, le=7)
    intrusion: int = Field(ge=1, le=7)
    creepiness: int = Field(ge=1, le=7)
    privacy_concern: int = Field(ge=1, le=7)
    trust: int = Field(ge=1, le=7)
    user_agency: int = Field(ge=1, le=7)
    rationale: str = Field(default="", max_length=1_000)
    skipped: bool = False


class StudySession(BaseModel):
    session_id: str
    participant_code: str
    protocol_version: str
    consented_at: datetime
    assignment_seed: int
    status: str = "active"

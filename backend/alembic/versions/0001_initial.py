"""initial research prototype tables"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "runs",
        sa.Column("run_id", sa.String(64), primary_key=True),
        sa.Column("campaign_id", sa.String(128), nullable=False),
        sa.Column("scenario_id", sa.String(160), nullable=False),
        sa.Column("scenario_version", sa.Integer, nullable=False),
        sa.Column("method", sa.String(64), nullable=False),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("prompt_hashes", sa.JSON, nullable=False),
        sa.Column("config_hash", sa.String(64), nullable=False),
        sa.Column("structured_result", sa.JSON, nullable=False),
        sa.Column("visible_reply", sa.Text, nullable=False),
        sa.Column("validation_status", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_runs_scenario_id", "runs", ["scenario_id"])
    op.create_index("ix_runs_method", "runs", ["method"])
    op.create_table(
        "study_sessions",
        sa.Column("session_id", sa.String(64), primary_key=True),
        sa.Column("participant_code", sa.String(64), unique=True, nullable=False),
        sa.Column("protocol_version", sa.String(64), nullable=False),
        sa.Column("consent_status", sa.Boolean, nullable=False),
        sa.Column("consented_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("assignment_seed", sa.Integer, nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("withdrawal_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "study_assignments",
        sa.Column("assignment_id", sa.String(64), primary_key=True),
        sa.Column(
            "session_id",
            sa.String(64),
            sa.ForeignKey("study_sessions.session_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("scenario_id", sa.String(160), nullable=False),
        sa.Column("blinded_response_ids", sa.JSON, nullable=False),
        sa.Column("display_order", sa.JSON, nullable=False),
        sa.Column("completion_status", sa.String(32), nullable=False),
    )
    op.create_table(
        "study_responses",
        sa.Column("response_id", sa.String(64), primary_key=True),
        sa.Column(
            "assignment_id",
            sa.String(64),
            sa.ForeignKey("study_assignments.assignment_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("ratings", sa.JSON, nullable=False),
        sa.Column("rationale", sa.Text, nullable=False),
        sa.Column("skipped", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("study_responses")
    op.drop_table("study_assignments")
    op.drop_table("study_sessions")
    op.drop_index("ix_runs_method", table_name="runs")
    op.drop_index("ix_runs_scenario_id", table_name="runs")
    op.drop_table("runs")

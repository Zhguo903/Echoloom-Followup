from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bbi.domain.runs import RunRecord
from bbi.storage.models import RunRow


class RunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, record: RunRecord) -> None:
        self.session.add(
            RunRow(
                run_id=record.run_id,
                campaign_id=record.campaign_id,
                scenario_id=record.scenario_id,
                scenario_version=record.scenario_version,
                method=record.method.value,
                provider=record.provider,
                model=record.model_id,
                prompt_hashes=record.prompt_hashes,
                config_hash=record.config_hash,
                structured_result=record.model_dump(mode="json"),
                visible_reply=record.visible_reply,
                validation_status="valid" if not record.validator_issues else "issues",
                created_at=record.created_at,
            )
        )
        await self.session.commit()

    async def get(self, run_id: str) -> RunRecord | None:
        row = await self.session.get(RunRow, run_id)
        return RunRecord.model_validate(row.structured_result) if row else None

    async def list(
        self, scenario_id: str | None = None, method: str | None = None
    ) -> list[RunRecord]:
        query = select(RunRow).order_by(RunRow.created_at.desc())
        if scenario_id:
            query = query.where(RunRow.scenario_id == scenario_id)
        if method:
            query = query.where(RunRow.method == method)
        rows = (await self.session.scalars(query)).all()
        return [RunRecord.model_validate(row.structured_result) for row in rows]

    async def clear(self) -> None:
        rows = (await self.session.scalars(select(RunRow))).all()
        for row in rows:
            await self.session.delete(row)
        await self.session.commit()

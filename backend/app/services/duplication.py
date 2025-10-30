from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Material, Session


class DuplicationService:
    """Handles duplication of lesson plans across groups with overrides."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def duplicate_plan(
        self,
        source_session_id: int,
        target_group_ids: list[int],
        scheduled_date: date | None = None,
    ) -> list[Session]:
        result = await self.session.execute(
            select(Session).where(Session.id == source_session_id)
        )
        source_session = result.scalar_one()
        duplicated_sessions: list[Session] = []

        for group_id in target_group_ids:
            new_session = Session(
                group_id=group_id,
                subject_id=source_session.subject_id,
                trimester_id=source_session.trimester_id,
                scheduled_date=scheduled_date or source_session.scheduled_date,
                lesson_plan=source_session.lesson_plan,
                override_plan=None,
                source_session_id=source_session.id,
            )
            self.session.add(new_session)
            await self.session.flush()

            material_stmt = select(Material).where(Material.session_id == source_session.id)
            materials = (await self.session.execute(material_stmt)).scalars().all()
            for material in materials:
                cloned = Material(
                    session_id=new_session.id,
                    title=material.title,
                    description=material.description,
                    url=material.url,
                    content_text=material.content_text,
                )
                self.session.add(cloned)

            duplicated_sessions.append(new_session)

        await self.session.commit()
        return duplicated_sessions

    async def override_plan(self, session_id: int, override_plan: str) -> Session:
        result = await self.session.execute(select(Session).where(Session.id == session_id))
        session = result.scalar_one()
        session.override_plan = override_plan
        await self.session.commit()
        await self.session.refresh(session)
        return session

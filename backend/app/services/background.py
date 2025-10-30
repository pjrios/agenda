from __future__ import annotations

import asyncio
from datetime import date
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session
from ..models import BackgroundJob, Material
from ..semantic.index import semantic_index


class BackgroundJobService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def schedule_embedding_refresh(self) -> BackgroundJob:
        job = BackgroundJob(
            job_type="semantic_refresh",
            status="queued",
            payload=None,
            created_at=date.today(),
            updated_at=date.today(),
        )
        self.session.add(job)
        await self.session.commit()
        asyncio.create_task(self._run_embedding_refresh(job.id))
        return job

    async def _run_embedding_refresh(self, job_id: int) -> None:
        async with async_session() as run_session:
            job = await run_session.get(BackgroundJob, job_id)
            if job is None:
                return
            job.status = "running"
            await run_session.commit()

            materials = await run_session.execute(select(Material))
            payload = [
                {
                    "id": material.id,
                    "title": material.title,
                    "description": material.description or "",
                    "content_text": material.content_text,
                }
                for material in materials.scalars().all()
            ]
            semantic_index.build(payload)

            job.status = "completed"
            job.updated_at = date.today()
            await run_session.commit()


async def bulk_index_materials(materials: Iterable[Material]) -> None:
    serialized = [
        {
            "id": material.id,
            "title": material.title,
            "description": material.description or "",
            "content_text": material.content_text,
        }
        for material in materials
    ]
    semantic_index.build(serialized)

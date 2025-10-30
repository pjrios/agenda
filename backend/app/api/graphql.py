from __future__ import annotations

from datetime import date
from typing import List, Optional

import strawberry
from sqlalchemy import select

from ..database import async_session
from ..models import Group, Session, Trimester


@strawberry.type
class SessionType:
    id: int
    group_id: int
    subject_id: int
    trimester_id: int
    scheduled_date: date
    lesson_plan: str
    override_plan: Optional[str]


@strawberry.type
class GroupType:
    id: int
    name: str
    level_id: int


@strawberry.type
class TrimesterType:
    id: int
    name: str
    level_id: int
    start_date: date
    end_date: date


@strawberry.type
class Query:
    @strawberry.field
    async def sessions(
        self, info, group_id: Optional[int] = None
    ) -> List[SessionType]:
        async with async_session() as session:
            stmt = select(Session)
            if group_id is not None:
                stmt = stmt.where(Session.group_id == group_id)
            results = (await session.execute(stmt)).scalars().all()
            return [
                SessionType(
                    id=item.id,
                    group_id=item.group_id,
                    subject_id=item.subject_id,
                    trimester_id=item.trimester_id,
                    scheduled_date=item.scheduled_date,
                    lesson_plan=item.lesson_plan,
                    override_plan=item.override_plan,
                )
                for item in results
            ]

    @strawberry.field
    async def groups(self, info) -> List[GroupType]:
        async with async_session() as session:
            results = (await session.execute(select(Group))).scalars().all()
            return [
                GroupType(id=item.id, name=item.name, level_id=item.level_id)
                for item in results
            ]

    @strawberry.field
    async def trimesters(
        self, info, level_id: Optional[int] = None
    ) -> List[TrimesterType]:
        async with async_session() as session:
            stmt = select(Trimester)
            if level_id is not None:
                stmt = stmt.where(Trimester.level_id == level_id)
            results = (await session.execute(stmt)).scalars().all()
            return [
                TrimesterType(
                    id=item.id,
                    name=item.name,
                    level_id=item.level_id,
                    start_date=item.start_date,
                    end_date=item.end_date,
                )
                for item in results
            ]


def create_schema() -> strawberry.Schema:
    return strawberry.Schema(query=Query)

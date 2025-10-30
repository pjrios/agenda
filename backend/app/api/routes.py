from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import (
    Attachment,
    Group,
    Level,
    Material,
    NoClassDay,
    Rubric,
    RubricAttachment,
    Schedule,
    Session,
    Subject,
    Trimester,
)
from ..schemas.base import (
    AttachmentCreate,
    AttachmentRead,
    GroupCreate,
    GroupRead,
    LevelCreate,
    LevelRead,
    MaterialCreate,
    MaterialRead,
    NoClassDayCreate,
    NoClassDayRead,
    RubricAttachmentCreate,
    RubricAttachmentRead,
    RubricCreate,
    RubricRead,
    ScheduleCreate,
    ScheduleRead,
    SessionCreate,
    SessionRead,
    SessionUpdate,
    SessionDuplicateRequest,
    SubjectCreate,
    SubjectRead,
    TrimesterCreate,
    TrimesterRead,
)
from ..semantic.index import semantic_index
from ..services.duplication import DuplicationService
from ..services.background import BackgroundJobService

router = APIRouter()


async def paginate(session: AsyncSession, stmt, schema) -> list[Any]:
    results = (await session.execute(stmt)).scalars().all()
    return [schema.from_orm(item) for item in results]


@router.post("/levels", response_model=LevelRead)
async def create_level(
    payload: LevelCreate, session: AsyncSession = Depends(get_session)
) -> LevelRead:
    level = Level(name=payload.name)
    session.add(level)
    await session.commit()
    await session.refresh(level)
    return LevelRead.from_orm(level)


@router.get("/levels", response_model=list[LevelRead])
async def list_levels(session: AsyncSession = Depends(get_session)) -> list[LevelRead]:
    return await paginate(session, select(Level), LevelRead)


@router.post("/subjects", response_model=SubjectRead)
async def create_subject(
    payload: SubjectCreate, session: AsyncSession = Depends(get_session)
) -> SubjectRead:
    subject = Subject(name=payload.name, level_id=payload.level_id)
    session.add(subject)
    await session.commit()
    await session.refresh(subject)
    return SubjectRead.from_orm(subject)


@router.get("/subjects", response_model=list[SubjectRead])
async def list_subjects(session: AsyncSession = Depends(get_session)) -> list[SubjectRead]:
    return await paginate(session, select(Subject), SubjectRead)


@router.post("/groups", response_model=GroupRead)
async def create_group(
    payload: GroupCreate, session: AsyncSession = Depends(get_session)
) -> GroupRead:
    group = Group(name=payload.name, level_id=payload.level_id)
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return GroupRead.from_orm(group)


@router.get("/groups", response_model=list[GroupRead])
async def list_groups(session: AsyncSession = Depends(get_session)) -> list[GroupRead]:
    return await paginate(session, select(Group), GroupRead)


@router.post("/trimesters", response_model=TrimesterRead)
async def create_trimester(
    payload: TrimesterCreate, session: AsyncSession = Depends(get_session)
) -> TrimesterRead:
    trimester = Trimester(**payload.dict())
    session.add(trimester)
    await session.commit()
    await session.refresh(trimester)
    return TrimesterRead.from_orm(trimester)


@router.get("/trimesters", response_model=list[TrimesterRead])
async def list_trimesters(
    session: AsyncSession = Depends(get_session), level_id: int | None = None
) -> list[TrimesterRead]:
    stmt = select(Trimester)
    if level_id is not None:
        stmt = stmt.where(Trimester.level_id == level_id)
    return await paginate(session, stmt, TrimesterRead)


@router.post("/schedules", response_model=ScheduleRead)
async def create_schedule(
    payload: ScheduleCreate, session: AsyncSession = Depends(get_session)
) -> ScheduleRead:
    schedule = Schedule(**payload.dict())
    session.add(schedule)
    await session.commit()
    await session.refresh(schedule)
    return ScheduleRead.from_orm(schedule)


@router.get("/schedules", response_model=list[ScheduleRead])
async def list_schedules(
    session: AsyncSession = Depends(get_session), group_id: int | None = None
) -> list[ScheduleRead]:
    stmt = select(Schedule)
    if group_id is not None:
        stmt = stmt.where(Schedule.group_id == group_id)
    return await paginate(session, stmt, ScheduleRead)


@router.post("/sessions", response_model=SessionRead)
async def create_session(
    payload: SessionCreate, session: AsyncSession = Depends(get_session)
) -> SessionRead:
    session_obj = Session(**payload.dict(exclude={"materials"}))
    session.add(session_obj)
    await session.flush()

    for material_payload in payload.materials:
        material = Material(**material_payload.dict(), session_id=session_obj.id)
        session.add(material)

    await session.commit()
    await session.refresh(session_obj)
    return SessionRead.from_orm(session_obj)


@router.get("/sessions", response_model=list[SessionRead])
async def list_sessions(
    session: AsyncSession = Depends(get_session), group_id: int | None = None
) -> list[SessionRead]:
    stmt = select(Session)
    if group_id is not None:
        stmt = stmt.where(Session.group_id == group_id)
    return await paginate(session, stmt, SessionRead)


@router.patch("/sessions/{session_id}", response_model=SessionRead)
async def update_session(
    session_id: int,
    payload: SessionUpdate,
    session: AsyncSession = Depends(get_session),
) -> SessionRead:
    result = await session.execute(select(Session).where(Session.id == session_id))
    session_obj = result.scalar_one_or_none()
    if session_obj is None:
        raise HTTPException(status_code=404, detail="Session not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(session_obj, field, value)
    await session.commit()
    await session.refresh(session_obj)
    return SessionRead.from_orm(session_obj)


@router.post("/materials", response_model=MaterialRead)
async def create_material(
    payload: MaterialCreate, session: AsyncSession = Depends(get_session)
) -> MaterialRead:
    material = Material(**payload.dict())
    session.add(material)
    await session.commit()
    await session.refresh(material)
    semantic_index.upsert(
        {
            "id": material.id,
            "title": material.title,
            "description": material.description or "",
            "content_text": material.content_text,
        }
    )
    background_service = BackgroundJobService(session)
    await background_service.schedule_embedding_refresh()
    return MaterialRead.from_orm(material)


@router.get("/materials", response_model=list[MaterialRead])
async def list_materials(
    session: AsyncSession = Depends(get_session), session_id: int | None = None
) -> list[MaterialRead]:
    stmt = select(Material)
    if session_id is not None:
        stmt = stmt.where(Material.session_id == session_id)
    return await paginate(session, stmt, MaterialRead)


@router.post("/attachments", response_model=AttachmentRead)
async def create_attachment(
    payload: AttachmentCreate, session: AsyncSession = Depends(get_session)
) -> AttachmentRead:
    attachment = Attachment(**payload.dict())
    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)
    return AttachmentRead.from_orm(attachment)


@router.post("/rubrics", response_model=RubricRead)
async def create_rubric(
    payload: RubricCreate, session: AsyncSession = Depends(get_session)
) -> RubricRead:
    rubric = Rubric(**payload.dict())
    session.add(rubric)
    await session.commit()
    await session.refresh(rubric)
    return RubricRead.from_orm(rubric)


@router.get("/rubrics", response_model=list[RubricRead])
async def list_rubrics(session: AsyncSession = Depends(get_session)) -> list[RubricRead]:
    return await paginate(session, select(Rubric), RubricRead)


@router.post("/rubric-attachments", response_model=RubricAttachmentRead)
async def attach_rubric(
    payload: RubricAttachmentCreate, session: AsyncSession = Depends(get_session)
) -> RubricAttachmentRead:
    attachment = RubricAttachment(**payload.dict())
    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)
    return RubricAttachmentRead.from_orm(attachment)


@router.post("/no-class-days", response_model=NoClassDayRead)
async def create_no_class_day(
    payload: NoClassDayCreate, session: AsyncSession = Depends(get_session)
) -> NoClassDayRead:
    ncd = NoClassDay(**payload.dict())
    session.add(ncd)
    await session.commit()
    await session.refresh(ncd)
    return NoClassDayRead.from_orm(ncd)


@router.get("/calendar/agenda", response_model=list[SessionRead])
async def get_calendar_agenda(
    start: date,
    end: date,
    session: AsyncSession = Depends(get_session),
    group_id: int | None = None,
) -> list[SessionRead]:
    stmt = select(Session).where(Session.scheduled_date.between(start, end))
    if group_id is not None:
        stmt = stmt.where(Session.group_id == group_id)
    return await paginate(session, stmt, SessionRead)


@router.post("/sessions/{session_id}/duplicate", response_model=list[SessionRead])
async def duplicate_session(
    session_id: int,
    payload: SessionDuplicateRequest,
    session: AsyncSession = Depends(get_session),
) -> list[SessionRead]:
    service = DuplicationService(session)
    duplicates = await service.duplicate_plan(
        session_id, payload.target_groups, scheduled_date=payload.scheduled_date
    )
    return [SessionRead.from_orm(item) for item in duplicates]


@router.post("/sessions/{session_id}/override", response_model=SessionRead)
async def override_session_plan(
    session_id: int,
    payload: SessionUpdate,
    session: AsyncSession = Depends(get_session),
) -> SessionRead:
    if payload.override_plan is None:
        raise HTTPException(status_code=400, detail="override_plan is required")
    service = DuplicationService(session)
    updated = await service.override_plan(session_id, payload.override_plan)
    return SessionRead.from_orm(updated)


@router.get("/semantic/search")
async def semantic_search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    return semantic_index.search(query, limit=limit)


@router.post("/semantic/refresh")
async def semantic_refresh(session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    service = BackgroundJobService(session)
    job = await service.schedule_embedding_refresh()
    return {"job_id": job.id, "status": job.status}

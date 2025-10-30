from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class LevelBase(BaseModel):
    name: str


class LevelCreate(LevelBase):
    pass


class LevelRead(LevelBase):
    id: int

    class Config:
        orm_mode = True


class SubjectBase(BaseModel):
    name: str
    level_id: int


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str
    level_id: int


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: int

    class Config:
        orm_mode = True


class TrimesterBase(BaseModel):
    name: str
    level_id: int
    start_date: date
    end_date: date


class TrimesterCreate(TrimesterBase):
    pass


class TrimesterRead(TrimesterBase):
    id: int

    class Config:
        orm_mode = True


class ScheduleBase(BaseModel):
    group_id: int
    subject_id: int
    weekday: int
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int

    class Config:
        orm_mode = True


class MaterialBase(BaseModel):
    session_id: int
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    content_text: str


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    id: int

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    group_id: int
    subject_id: int
    trimester_id: int
    scheduled_date: date
    lesson_plan: str
    override_plan: Optional[str] = None
    source_session_id: Optional[int] = None


class SessionCreate(SessionBase):
    materials: list[MaterialCreate] = []


class SessionUpdate(BaseModel):
    lesson_plan: Optional[str] = None
    override_plan: Optional[str] = None


class SessionRead(SessionBase):
    id: int

    class Config:
        orm_mode = True


class SessionDuplicateRequest(BaseModel):
    target_groups: list[int]
    scheduled_date: Optional[date] = None


class RubricBase(BaseModel):
    subject_id: int
    name: str
    criteria: str


class RubricCreate(RubricBase):
    pass


class RubricRead(RubricBase):
    id: int

    class Config:
        orm_mode = True


class RubricAttachmentBase(BaseModel):
    rubric_id: int
    session_id: int
    notes: Optional[str] = None


class RubricAttachmentCreate(RubricAttachmentBase):
    pass


class RubricAttachmentRead(RubricAttachmentBase):
    id: int

    class Config:
        orm_mode = True


class AttachmentBase(BaseModel):
    material_id: int
    filename: str
    url: str


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentRead(AttachmentBase):
    id: int

    class Config:
        orm_mode = True


class NoClassDayBase(BaseModel):
    level_id: Optional[int] = None
    group_id: Optional[int] = None
    date: date
    reason: Optional[str] = None
    is_holiday: bool = False


class NoClassDayCreate(NoClassDayBase):
    pass


class NoClassDayRead(NoClassDayBase):
    id: int

    class Config:
        orm_mode = True

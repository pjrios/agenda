from __future__ import annotations

from datetime import date, time
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    subjects: Mapped[list[Subject]] = relationship("Subject", back_populates="level")
    groups: Mapped[list[Group]] = relationship("Group", back_populates="level")
    trimesters: Mapped[list[Trimester]] = relationship(
        "Trimester", back_populates="level", cascade="all, delete-orphan"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"))

    level: Mapped[Level] = relationship("Level", back_populates="subjects")
    schedules: Mapped[list[Schedule]] = relationship("Schedule", back_populates="subject")
    sessions: Mapped[list[Session]] = relationship("Session", back_populates="subject")
    rubrics: Mapped[list[Rubric]] = relationship("Rubric", back_populates="subject")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"))

    level: Mapped[Level] = relationship("Level", back_populates="groups")
    schedules: Mapped[list[Schedule]] = relationship(
        "Schedule", back_populates="group", cascade="all, delete-orphan"
    )
    sessions: Mapped[list[Session]] = relationship("Session", back_populates="group")


class Trimester(Base):
    __tablename__ = "trimesters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    level: Mapped[Level] = relationship("Level", back_populates="trimesters")
    sessions: Mapped[list[Session]] = relationship("Session", back_populates="trimester")


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    group: Mapped[Group] = relationship("Group", back_populates="schedules")
    subject: Mapped[Subject] = relationship("Subject", back_populates="schedules")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    trimester_id: Mapped[int] = mapped_column(ForeignKey("trimesters.id", ondelete="CASCADE"))
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    lesson_plan: Mapped[str] = mapped_column(Text, nullable=False)
    override_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_session_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True
    )

    group: Mapped[Group] = relationship("Group", back_populates="sessions")
    subject: Mapped[Subject] = relationship("Subject", back_populates="sessions")
    trimester: Mapped[Trimester] = relationship("Trimester", back_populates="sessions")
    materials: Mapped[list[Material]] = relationship(
        "Material", back_populates="session", cascade="all, delete-orphan"
    )
    rubric_attachments: Mapped[list[RubricAttachment]] = relationship(
        "RubricAttachment", back_populates="session", cascade="all, delete-orphan"
    )
    source_session: Mapped[Optional[Session]] = relationship(remote_side="Session.id")


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[Session] = relationship("Session", back_populates="materials")
    attachments: Mapped[list[Attachment]] = relationship(
        "Attachment", back_populates="material", cascade="all, delete-orphan"
    )


class Rubric(Base):
    __tablename__ = "rubrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    criteria: Mapped[str] = mapped_column(Text, nullable=False)

    subject: Mapped[Subject] = relationship("Subject", back_populates="rubrics")
    attachments: Mapped[list[RubricAttachment]] = relationship(
        "RubricAttachment", back_populates="rubric", cascade="all, delete-orphan"
    )


class RubricAttachment(Base):
    __tablename__ = "rubric_attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rubric_id: Mapped[int] = mapped_column(ForeignKey("rubrics.id", ondelete="CASCADE"))
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    rubric: Mapped[Rubric] = relationship("Rubric", back_populates="attachments")
    session: Mapped[Session] = relationship("Session", back_populates="rubric_attachments")


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id", ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    material: Mapped[Material] = relationship("Material", back_populates="attachments")


class NoClassDay(Base):
    __tablename__ = "no_class_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level_id: Mapped[Optional[int]] = mapped_column(ForeignKey("levels.id"), nullable=True)
    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("groups.id"), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_holiday: Mapped[bool] = mapped_column(Boolean, default=False)


class BackgroundJob(Base):
    __tablename__ = "background_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=False)

"""initial schema"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "levels",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
    )

    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id", ondelete="CASCADE")),
    )

    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id", ondelete="CASCADE")),
    )

    op.create_table(
        "trimesters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id", ondelete="CASCADE")),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
    )

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE")),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subjects.id", ondelete="CASCADE")),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
    )

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE")),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subjects.id", ondelete="CASCADE")),
        sa.Column("trimester_id", sa.Integer(), sa.ForeignKey("trimesters.id", ondelete="CASCADE")),
        sa.Column("scheduled_date", sa.Date(), nullable=False),
        sa.Column("lesson_plan", sa.Text(), nullable=False),
        sa.Column("override_plan", sa.Text(), nullable=True),
        sa.Column("source_session_id", sa.Integer(), sa.ForeignKey("sessions.id", ondelete="SET NULL")),
    )

    op.create_table(
        "materials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id", ondelete="CASCADE")),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=255), nullable=True),
        sa.Column("content_text", sa.Text(), nullable=False),
    )

    op.create_table(
        "rubrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subjects.id", ondelete="CASCADE")),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("criteria", sa.Text(), nullable=False),
    )

    op.create_table(
        "rubric_attachments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("rubric_id", sa.Integer(), sa.ForeignKey("rubrics.id", ondelete="CASCADE")),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id", ondelete="CASCADE")),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    op.create_table(
        "attachments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id", ondelete="CASCADE")),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=255), nullable=False),
    )

    op.create_table(
        "no_class_days",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=True),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id"), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=True),
        sa.Column("is_holiday", sa.Boolean(), nullable=False, server_default=sa.text("0")),
    )

    op.create_table(
        "background_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("created_at", sa.Date(), nullable=False),
        sa.Column("updated_at", sa.Date(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("background_jobs")
    op.drop_table("no_class_days")
    op.drop_table("attachments")
    op.drop_table("rubric_attachments")
    op.drop_table("rubrics")
    op.drop_table("materials")
    op.drop_table("sessions")
    op.drop_table("schedules")
    op.drop_table("trimesters")
    op.drop_table("groups")
    op.drop_table("subjects")
    op.drop_table("levels")

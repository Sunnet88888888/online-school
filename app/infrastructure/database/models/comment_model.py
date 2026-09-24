from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.infrastructure.database.models.base import Base


class CommentModel(Base):
    __tablename__ = 'comments'

    __table_args__ = (
        CheckConstraint(
            """
            (
                CASE WHEN lecture_id IS NOT NULL THEN 1 ELSE 0 END +
                CASE WHEN question_id IS NOT NULL THEN 1 ELSE 0 END +
                CASE WHEN task_id IS NOT NULL THEN 1 ELSE 0 END +
                CASE WHEN code_task_id IS NOT NULL THEN 1 ELSE 0 END
            ) = 1
            """,
            name='ck_comments_exactly_one_target',
        ),
        Index(
            'ix_comments_lecture_created_at',
            'lecture_id',
            'created_at',
            'id',
        ),
        Index(
            'ix_comments_task_created_at',
            'task_id',
            'created_at',
            'id',
        ),
        Index(
            'ix_comments_code_task_created_at',
            'code_task_id',
            'created_at',
            'id',
        ),
        Index(
            'ix_comments_question_created_at',
            'question_id',
            'created_at',
            'id',
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    lecture_id: Mapped[str | None] = mapped_column(
        ForeignKey('lectures.id', ondelete='CASCADE'),
        nullable=True,
    )

    question_id: Mapped[str | None] = mapped_column(
        ForeignKey('questions.id', ondelete='CASCADE'),
        nullable=True,
    )

    task_id: Mapped[str | None] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        nullable=True,
    )

    code_task_id: Mapped[str | None] = mapped_column(
        ForeignKey('code_tasks.id', ondelete='CASCADE'),
        nullable=True,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID
from app.domain.exceptions import InvalidCommentError


class CommentTargetType(StrEnum):
    LECTURE = 'lecture'
    QUESTION = 'question'
    TASK = 'task'
    CODE_TASK = 'code_task'


@dataclass(frozen=True, slots=True)
class CommentTarget:
    type: CommentTargetType
    id: UUID


@dataclass(slots=True)
class Comment:
    id: UUID
    target: CommentTarget
    user_id: UUID
    text: str
    created_at: datetime
    updated_at: datetime | None

    def __post_init__(self) -> None:
        self._validate_text()

    def _validate_text(self) -> None:
        if not self.text or not self.text.strip():
            raise InvalidCommentError(
                'Comment text cannot be empty.'
            )

        if len(self.text) > 2000:
            raise InvalidCommentError(
                'Comment text cannot exceed 2000 characters.'
            )

    def update_text(self, text: str, updated_at: datetime) -> None:
        self.text = text
        self.updated_at = updated_at
        self._validate_text()
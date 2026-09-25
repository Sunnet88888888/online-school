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
        self.text = self._normalize_and_validate_text(self.text)

    def update_text(self, text: str, updated_at: datetime) -> None:
        text = self._normalize_and_validate_text(text)

        self.text = text
        self.updated_at = updated_at

    @staticmethod
    def _normalize_and_validate_text(text: str) -> str:
        text = text.strip()

        if not text:
            raise InvalidCommentError(
                'Comment text cannot be empty.'
            )

        if len(text) > 2000:
            raise InvalidCommentError(
                'Comment text cannot exceed 2000 characters.'
            )

        return text
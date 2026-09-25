from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.domain.entities.comment import CommentTargetType

@dataclass(frozen=True, slots=True)
class CommentDTO:
    id: UUID
    user_id: UUID
    target_type: CommentTargetType
    target_id: UUID
    text: str
    created_at: datetime
    updated_at: datetime | None
from dataclasses import dataclass
from uuid import UUID
from app.domain.entities.user import User
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.comment import Comment
from datetime import datetime, timezone
from app.application.exceptions import CommentNotFoundError, PermissionDeniedError
from app.application.dto.comments import CommentDTO


@dataclass(frozen=True, slots=True)
class UpdateCommentCommand:
    actor: User
    comment_id: UUID
    text: str


class UpdateCommentUseCase:

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self,
        command: UpdateCommentCommand,
    ) -> Comment:
        comment = await self.uow.comments.get_by_id(command.comment_id)

        if comment is None:
            raise CommentNotFoundError("Comment not found.")

        if comment.user_id != command.actor.id:
            raise PermissionDeniedError("Only comment author can edit this comment")

        comment.update_text(command.text, updated_at=datetime.now(timezone.utc))

        async with self.uow:
            await self.uow.comments.update(comment)
            await self.uow.commit()

        return CommentDTO(
            id=comment.id,
            user_id=comment.user_id,
            text=comment.text,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )

from dataclasses import dataclass
from uuid import UUID
from app.domain.entities.user import User
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.exceptions import CommentNotFoundError, PermissionDeniedError
from app.application.services.content_target_resolver import ContentTargetResolver


@dataclass(frozen=True, slots=True)
class DeleteCommentCommand:
    actor: User
    comment_id: UUID


class DeleteCommentUseCase:

    def __init__(
        self,
        uow: UnitOfWork,
        resolver: ContentTargetResolver,
    ) -> None:
        self.uow = uow
        self.resolver = resolver

    async def execute(
        self,
        command: DeleteCommentCommand,
    ) -> None:

        comment = await self.uow.comments.get_by_id(command.comment_id)

        if comment is None:
            raise CommentNotFoundError("Comment not found")

        if command.actor.can_manage_platform():
            pass

        elif command.actor.is_student():
            if comment.user_id != command.actor.id:
                raise PermissionDeniedError(
                    "Students can remove only their own comments."
                )
        elif command.actor.is_author():
            resolved_item = await self.resolver.resolve(comment.target)
            if resolved_item.course.author_id != command.actor.id:
                raise PermissionDeniedError(
                    "Authors can remove only comments from their own courses."
                )
        else:
            raise PermissionDeniedError(
                "You do not have permission to remove this comment."
            )
        async with self.uow:
            await self.uow.comments.remove(command.comment_id)
            await self.uow.commit()


from dataclasses import dataclass
from app.domain.entities.user import User
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.exceptions import PermissionDeniedError
from app.application.dto.comments import CommentDTO
from app.domain.entities.comment import CommentTarget
from app.application.services.course_content_access_service import CourseContentAccessService
from app.application.services.content_target_resolver import ContentTargetResolver




@dataclass(frozen=True, slots=True)
class GetCommentsCommand:
    actor: User
    target: CommentTarget
    
    


class GetCommentsUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        resolver: ContentTargetResolver,
        access_service: CourseContentAccessService,
    ) -> None:
        self.uow = uow
        self.resolver = resolver
        self.access_service = access_service

    async def execute(
        self,
        command: GetCommentsCommand,
    ) -> list[CommentDTO]:

        resolved_target = await self.resolver.resolve(
            target=command.target,
        )

        allowed = await self.access_service.can_view_course(
            course_id=resolved_target.course.id,
            actor=command.actor,
        )

        if not allowed:
            raise PermissionDeniedError(
                "You cannot view comments for this content."
            )

        async with self.uow:
            comments = await self.uow.comments.list_by_target(
                command.target,
            )

        return [
            CommentDTO(
                id=comment.id,
                user_id=comment.user_id,
                target_type=comment.target.type,
                target_id=comment.target.id,
                text=comment.text,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
            )
            for comment in comments
        ]
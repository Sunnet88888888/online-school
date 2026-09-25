from dataclasses import dataclass
from uuid import uuid4
from app.domain.entities.user import User
from app.domain.entities.comment import CommentTarget
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.content_target_resolver import ContentTargetResolver
from app.application.services.course_content_access_service import CourseContentAccessService
from app.domain.entities.comment import Comment
from datetime import datetime , timezone
from app.application.exceptions import PermissionDeniedError
from app.application.dto.comments import CommentDTO


@dataclass(frozen=True, slots=True)
class CreateCommentCommand:
    actor: User
    target: CommentTarget
    text: str
    
    
    
class CreateCommentUseCase:

    def __init__(
        self,
        uow: UnitOfWork,
        resolver: ContentTargetResolver ,
        access_service: CourseContentAccessService,
    ) -> None:
        self.uow = uow
        self.resolver = resolver
        self.access_service = access_service

    async def execute(
        self,
        command: CreateCommentCommand,
    ) -> Comment:
        resolved_target = await self.resolver.resolve(
            command.target
        )
        
        ## Actually, we need to implement enrollment . After enrollment add new logic to check if student joined to course or not 
        ## Enrolled students , author and admin can write comments, don't forget to implement this logic 
        
        allowed = await self.access_service.can_comment_on_course_content(
            course=resolved_target.course,
            actor=command.actor,
        )

        if not allowed:
            raise PermissionDeniedError(
                'You cannot comment on this content.'
            )

        comment = Comment(
            id=uuid4(),
            target=command.target,
            user_id=command.actor.id,
            text=command.text,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )

        async with self.uow:
            await self.uow.comments.add(comment)
            await self.uow.commit()

        return CommentDTO(
            id=comment.id,
            user_id=comment.user_id,
            target_type=comment.target.type,
            target_id=comment.target.id,
            text=comment.text,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
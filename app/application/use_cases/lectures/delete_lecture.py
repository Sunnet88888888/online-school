from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.exceptions import LectureNotFoundError
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User


@dataclass(slots=True)
class DeleteLectureCommand:
    actor: User
    lecture_id: UUID


class DeleteLectureUseCase:

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteLectureCommand) -> None:
        async with self.uow:
            lecture = await self.uow.lectures.get_by_id(command.lecture_id)

            if lecture is None:
                raise LectureNotFoundError("Lecture not found.")

            await self.course_access_service.ensure_can_manage_section(
                actor=command.actor, section_id=lecture.section_id
            )

            section = await self.uow.sections.get_by_id(lecture.section_id)

            section.remove_lecture(command.lecture_id)

            await self.uow.sections.update(section)
            await self.uow.lectures.remove(command.lecture_id)

            await self.uow.commit()

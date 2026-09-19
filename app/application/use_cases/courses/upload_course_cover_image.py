from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from app.application.dto.uploaded_files import UploadedFile
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.protocols.file_storage import FileStorage
from app.application.protocols.image_processor import ImageProcessor
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.course import Course
from app.domain.entities.user import User
from app.application.services.course_image_validator import ImageValidationService


@dataclass(slots=True)
class UploadCourseCoverImageCommand:
    course_id: UUID
    actor: User
    file: UploadedFile


class UploadCourseCoverImageUseCase:

    def __init__(
        self, 
        uow: UnitOfWork, 
        image_validation_service: ImageValidationService,
        image_processor: ImageProcessor,
        file_storage: FileStorage,
    ) -> None:
        self.uow = uow
        self.image_validation_service = image_validation_service
        self.image_processor = image_processor
        self.file_storage = file_storage
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: UploadCourseCoverImageCommand) -> Course:
        async with self.uow:

            course = await self.course_access_service.ensure_can_manage_course(
                actor=command.actor,
                course_id=command.course_id,
            )

            await self.image_validation_service.validate(
                filename=command.file.filename, content_type=command.file.content_type
            )
            
            self.image_processor.validate(command.file.stream)
            
            extension = Path(command.file.filename).suffix.lower()
            data = command.file.stream.getvalue()
            
            image_file_name = await self.file_storage.save(data=data, extension=extension)
            
            image_url = f"/media/{image_file_name}"
            
            course.cover_image_url = image_url
            
            await self.uow.courses.update(course)
            await self.uow.commit()
            return course
            
            

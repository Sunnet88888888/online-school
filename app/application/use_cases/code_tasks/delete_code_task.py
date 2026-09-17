from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.exceptions import CodeTaskAlreadyUsedError, CodeTaskNotFoundError
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User




@dataclass(slots=True)
class DeleteCodeTaskCommand:
    actor: User
    code_task_id: UUID
    
    
    
class DeleteCodeTaskUseCase:
    
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)
        
    async def execute(self, command: DeleteCodeTaskCommand) -> None:
        async with self.uow:
            code_task = await self.uow.code_tasks.get_by_id(command.code_task_id)
            
            if code_task is None :
                raise CodeTaskNotFoundError("Code task not found.")
            
            await self.course_access_service.ensure_can_manage_section(
                actor=command.actor, section_id=code_task.section_id
            )
            
            has_code_submissions = await self.uow.code_submissions.exists_by_code_task_id(
                code_task_id=code_task.id
            )
            
            if has_code_submissions:
                raise CodeTaskAlreadyUsedError(
                    "Code Task already has student code submissions and cannot be changed safely."
                )
                
            section = await self.uow.sections.get_by_id(code_task.section_id)
            
            section.remove_code_task(command.code_task_id)
            
            await self.uow.sections.update(section)
            await self.uow.code_tasks.remove(command.code_task_id)
            
            await self.uow.commit()
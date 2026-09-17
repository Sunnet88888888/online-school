from dataclasses import dataclass
from uuid import UUID


from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.exceptions import CodeTaskAlreadyUsedError, CodeTaskNotFoundError, TestCaseNotFoundError
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User




@dataclass(slots=True)
class DeleteTestCaseCommand:
    actor: User
    test_case_id: UUID
    
    
class DeleteTestCaseUseCase:
    
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)
        
    
    async def execute(self, command: DeleteTestCaseCommand) -> None:
        async with self.uow:
            test_case = await self.uow.test_cases.get_by_id(command.test_case_id)
            
            
            if test_case is None :
                raise TestCaseNotFoundError("Test case not found.")
            
            
            code_task = await self.uow.code_tasks.get_by_id(code_task_id=test_case.code_task_id)
            
            if code_task is None:
                raise CodeTaskNotFoundError("Linked to this test case Code task not found.") 
            
            code_task.test_case_ids = [test_case.id for test_case in await self.uow.test_cases.list_by_code_task_id(code_task.id)]
                        
            
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
            
            code_task.remove_test_case(command.test_case_id)
            code_task.ensure_test_cases_configuration()
            
            
            
            await self.uow.code_tasks.update(code_task)
            await self.uow.test_cases.remove(command.test_case_id)
            
            await self.uow.commit()
            
              
from dataclasses import dataclass
from uuid import UUID


from app.application.exceptions import ModuleNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteModuleCommand:
    module_id: UUID
    
    
    
class DeleteModuleUseCase:
    
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        
    async def execute(self, command: DeleteModuleCommand) -> None:
        async with self.uow: 
            
            module = await self.uow.modules.get_by_id(command.module_id)
            
            if module is None:
                raise ModuleNotFoundError("Module not found.")
            
            course = await self.uow.courses.get_by_id(module.course_id)

            course.remove_module(command.module_id)
            
            await self.uow.courses.update(course=course)
            await self.uow.modules.remove(module_id=command.module_id)

            await self.uow.commit()
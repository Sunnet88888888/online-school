from dataclasses import dataclass
from uuid import UUID


from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteSectionCommand:
    section_id: UUID
    
    
    
class DeleteSectionUseCase:
    
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        
    async def execute(self, command: DeleteSectionCommand) -> None:
        async with self.uow: 
            
            section = await self.uow.sections.get_by_id(command.section_id)

            if section is None:
                raise SectionNotFoundError("Section not found.")
            
            module = await self.uow.modules.get_by_id(section.module_id)

            module.remove_section(section_id=command.section_id)

            await self.uow.modules.update(module=module)
            await self.uow.sections.remove(command.section_id)

            await self.uow.commit()
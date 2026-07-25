from dataclasses import dataclass
from uuid import uuid4

from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.course import Course

@dataclass(slots=True)
class CreateCourseCommand:
    title: str
    description: str
    

class CreateCourseUseCase:
    
    def __init__(self, uof: UnitOfWork) -> None:
        self.uof = uof
        
    async def execute(self, command: CreateCourseCommand) -> Course:
        async with self.uof:
            course = Course(
                id = uuid4(),
                title = command.title,
                description=command.description,
            )
            await self.uof.courses.add(course)
            await self.uof.commit()
            return course
        
        
        
        
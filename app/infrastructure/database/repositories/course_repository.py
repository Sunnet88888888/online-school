from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.interfaces.repositories.course_repository import CourseRepository
from app.domain.entities.course import Course
from app.infrastructure.database.mappers.course_mapper import CourseMapper
from app.infrastructure.database.models.course_model import CourseModel


class SqlAlchemyCourseRepository(CourseRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, course_id: UUID) -> Course | None:
        
        stmt = (
            select(CourseModel)
            .options(selectinload(CourseModel.modules))
            .where(CourseModel.id == str(course_id))
        )
        
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        return None if model is None else CourseMapper.to_doamin(model)
    
    
    

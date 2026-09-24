from dataclasses import dataclass
from uuid import UUID
from app.application.interfaces.repositories import (
    LectureRepository,
    TaskRepository,
    CodeTaskRepository,
    QuestionRepository,
    SectionRepository,
    ModuleRepository,
    CourseRepository,
    )

from app.domain.entities.comment import CommentTarget, CommentTargetType
from app.domain.entities.course import Course
from app.application.exceptions import (
    LectureNotFoundError,
    QuestionNotFoundError,
    TaskNotFoundError,
    CodeTaskNotFoundError,
    SectionNotFoundError,
    ModuleNotFoundError,
    CourseNotFoundError,
)


@dataclass(frozen=True, slots=True)
class ResolvedContentTarget:
    section_id: UUID
    course: Course

    
    
    
class ContentTargetResolver:

    def __init__(
        self,
        lecture_repository: LectureRepository,
        task_repository: TaskRepository,
        code_task_repository: CodeTaskRepository,
        question_repository: QuestionRepository,
        section_repository: SectionRepository,
        module_repository: ModuleRepository,
        course_repository: CourseRepository,
    ):
        self.lecture_repository = lecture_repository
        self.task_repository = task_repository
        self.code_task_repository = code_task_repository
        self.question_repository = question_repository
        self.section_repository = section_repository
        self.module_repository = module_repository
        self.course_repository = course_repository
        
    async def resolve(
    self,
    target: CommentTarget,
) -> ResolvedContentTarget:
        if target.type == CommentTargetType.LECTURE:
            lecture = await self.lecture_repository.get_by_id(target.id)
            if lecture is None:
                raise LectureNotFoundError('Lecture not found.')
            section = await self.section_repository.get_by_id(lecture.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')
            module = await self.module_repository.get_by_id(section.module_id)
            if module is None:
                raise ModuleNotFoundError('Module not found.')
            course = await self.course_repository.get_by_id(module.course_id)
            if course is None:
                raise CourseNotFoundError('Course not found.')
            return ResolvedContentTarget(section_id=section.id, course=course)

        elif target.type == CommentTargetType.TASK:
            task = await self.task_repository.get_by_id(target.id)
            if task is None:
                raise TaskNotFoundError('Task not found.')
            section = await self.section_repository.get_by_id(task.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')
            module = await self.module_repository.get_by_id(section.module_id)
            if module is None:
                raise ModuleNotFoundError('Module not found.')
            course = await self.course_repository.get_by_id(module.course_id)
            if course is None:
                raise CourseNotFoundError('Course not found.')
            return ResolvedContentTarget(section_id=section.id, course=course)

        elif target.type == CommentTargetType.CODE_TASK:
            code_task = await self.code_task_repository.get_by_id(target.id)
            if code_task is None:
                raise CodeTaskNotFoundError('CodeTask not found.')
            section = await self.section_repository.get_by_id(code_task.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')
            module = await self.module_repository.get_by_id(section.module_id)
            if module is None:
                raise ModuleNotFoundError('Module not found.')
            course = await self.course_repository.get_by_id(module.course_id)
            if course is None:
                raise CourseNotFoundError('Course not found.')
            return ResolvedContentTarget(section_id=section.id, course=course)

        elif target.type == CommentTargetType.QUESTION:
            question = await self.question_repository.get_by_id(target.id)
            if question is None:
                raise QuestionNotFoundError('Question not found.')
            section = await self.section_repository.get_by_id(question.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')
            module = await self.module_repository.get_by_id(section.module_id)
            if module is None:
                raise ModuleNotFoundError('Module not found.')
            course = await self.course_repository.get_by_id(module.course_id)
            if course is None:
                raise CourseNotFoundError('Course not found.')
            return ResolvedContentTarget(section_id=section.id, course=course)

        raise ValueError(f'Unsupported comment target type: {target.type}')
        
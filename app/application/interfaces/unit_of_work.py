from abc import ABC, abstractmethod

from app.application.interfaces.repositories import (
    CourseRepository,
    LectureRepository,
    SectionRepository,
    ModuleRepository,
    QuestionRepository,
    AnswerOptionRepository,
    QuestionAttemptRepository,
    UserRepository,
    ProgressRepository,
    TaskRepository,
    TaskAttemptRepository,
    CodeTaskRepository,
    TestCaseRepository,
    
)



class UnitOfWork(ABC):
    courses: CourseRepository
    modules: ModuleRepository
    sections: SectionRepository
    lectures: LectureRepository
    questions: QuestionRepository
    answer_options: AnswerOptionRepository
    question_attempts: QuestionAttemptRepository
    users: UserRepository
    progress: ProgressRepository
    tasks: TaskRepository
    task_attempts: TaskAttemptRepository
    code_tasks: CodeTaskRepository
    test_cases: TestCaseRepository

    
    
    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        raise NotImplementedError
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

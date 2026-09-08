from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.task_attempt import TaskAttempt



class TaskAttemptRepository(ABC):
    @abstractmethod
    async def add(self, task_attempt: TaskAttempt) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, task_attempt_id: UUID) -> TaskAttempt | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_task_id(self, task_id: UUID) -> list[TaskAttempt]:
        raise NotImplementedError
    
    @abstractmethod
    async def exists_by_task_id(self, task_id: UUID) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, task_attempt: TaskAttempt) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_attempt_id: UUID) -> None:
        raise NotImplementedError
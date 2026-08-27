from uuid import UUID

import pytest 

class FakeCourseRepository:
    def __init__(self) -> None:
        self.items = {}
        
    async def get_by_id(self, course_id):
        return self.items.get(course_id)
    
    async def list(self):
        return list(self.items.values())
    
    async def add(self, course) -> None:
        self.items[course.id] = course
    
    async def update(self, course) -> None:
        self.items[course.id] = course
        
    async def remove(self, course_id: UUID) -> None:
        self.items.pop(course_id, None)


class FakeModuleRepository:
    def __init__(self) -> None:
        self.items = {}

    async def get_by_id(self, module_id):
        return self.items.get(module_id)

    async def get_by_ids(self, module_ids):
        return [self.items[module_id] for module_id in module_ids if module_id in self.items]

    async def add(self, module) -> None:
        self.items[module.id] = module

    async def update(self, module) -> None:
        self.items[module.id] = module
        
    async def remove(self, module_id: UUID) -> None:
        self.items.pop(module_id, None)
        

class FakeSectionRepository:
    def __init__(self) -> None:
        self.items = {}

    async def get_by_id(self, section_id):
        return self.items.get(section_id)

    async def get_by_ids(self, section_ids):
        return [self.items[section_id] for section_id in section_ids if section_id in self.items]

    async def add(self, section) -> None:
        self.items[section.id] = section

    async def update(self, section) -> None:
        self.items[section.id] = section
        
    async def remove(self, section_id: UUID):
        self.items.pop(section_id, None)
        


class FakeLectureRepository:
    def __init__(self) -> None:
        self.items = {}

    async def get_by_id(self, lecture_id):
        return self.items.get(lecture_id)

    async def get_by_ids(self, lecture_ids):
        return [self.items[lecture_id] for lecture_id in lecture_ids if lecture_id in self.items]

    async def add(self, lecture) -> None:
        self.items[lecture.id] = lecture

    async def update(self, lecture) -> None:
        self.items[lecture.id] = lecture
        
    async def remove(self, lecture_id: UUID):
        self.items.pop(lecture_id, None)
        


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.course_repository = FakeCourseRepository()
        self.module_repository = FakeModuleRepository()
        self.section_repository = FakeSectionRepository()
        self.lecture_repository = FakeLectureRepository()
        self.users = None
        self.committed = False
        self.rolled_back = False
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            await self.rollback()
            
    async def commit(self) -> None:
        self.committed = True
    
    async def rollback(self) -> None:
        self.rolled_back = True
    
    
@pytest.mark.asyncio

    
    
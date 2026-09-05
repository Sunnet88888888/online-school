from uuid import UUID, uuid4

import pytest

from app.application.exceptions import CourseNotFoundError, LectureNotFoundError, SectionNotFoundError, ModuleNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.courses.create_course import CreateCourseCommand, CreateCourseUseCase
from app.application.use_cases.courses.delete_course import DeleteCourseCommand, DeleteCourseUseCase
from app.application.use_cases.lectures.delete_lecture import DeleteLectureCommand, DeleteLectureUseCase
from app.application.use_cases.modules.delete_module import DeleteModuleCommand, DeleteModuleUseCase
from app.application.use_cases.sections.delete_section import DeleteSectionCommand, DeleteSectionUseCase
from app.domain.entities.course import Course
from app.domain.entities.lecture import Lecture
from app.domain.entities.module import Module
from app.domain.entities.section import Section
from tests.unit.application.test_content_write_use_cases import make_author 

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
        


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.courses = FakeCourseRepository()
        self.modules = FakeModuleRepository()
        self.sections = FakeSectionRepository()
        self.lectures = FakeLectureRepository()
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





@pytest.fixture
async def course_tree():
    uow = FakeUnitOfWork()
    actor = make_author()

    # IDs
    course_id = uuid4()
    module_a_id = uuid4()
    module_b_id = uuid4()

    section_a_id = uuid4()
    section_b_id = uuid4()
    section_c_id = uuid4()

    lecture_1_id = uuid4()
    lecture_2_id = uuid4()
    lecture_3_id = uuid4()
    lecture_4_id = uuid4()

    # Course
    course = Course(
        
        id=course_id,
        author_id=actor.id,
        title="Test Course",
        description="Test description",
    )

    # Modules
    module_a = Module(
        id=module_a_id,
        course_id=course_id,
        title="Module A",
        description="Module A description",
        position=1,
    )

    module_b = Module(
        id=module_b_id,
        course_id=course_id,
        title="Module B",
        description="Module B description",
        position=2,
    )

    # Sections
    section_a = Section(
        id=section_a_id,
        module_id=module_a_id,
        title="Section A",
        description="Section A description",
        position=1,
    )

    section_b = Section(
        id=section_b_id,
        module_id=module_a_id,
        title="Section B",
        description="Section B description",
        position=2,
    )

    section_c = Section(
        id=section_c_id,
        module_id=module_b_id,
        title="Section C",
        description="Section C description",
        position=1,
    )

    # Lectures
    lecture_1 = Lecture(
        id=lecture_1_id,
        section_id=section_a_id,
        title="Lecture 1",
        content="Lecture 1 content",
        position=1,
    )

    lecture_2 = Lecture(
        id=lecture_2_id,
        section_id=section_a_id,
        title="Lecture 2",
        content="Lecture 2 content",
        position=2,
    )

    lecture_3 = Lecture(
        id=lecture_3_id,
        section_id=section_b_id,
        title="Lecture 3",
        content="Lecture 3 content",
        position=1,
    )

    lecture_4 = Lecture(
        id=lecture_4_id,
        section_id=section_c_id,
        title="Lecture 4",
        content="Lecture 4 content",
        position=1,
    )

    # Build relationships
    course.module_ids = [module_a_id, module_b_id]

    module_a.section_ids = [section_a_id, section_b_id]
    module_b.section_ids = [section_c_id]

    section_a.lecture_ids = [lecture_1_id, lecture_2_id]
    section_b.lecture_ids = [lecture_3_id]
    section_c.lecture_ids = [lecture_4_id]

    # Put everything into fake repositories
    await uow.courses.add(course)

    await uow.modules.add(module_a)
    await uow.modules.add(module_b)

    await uow.sections.add(section_a)
    await uow.sections.add(section_b)
    await uow.sections.add(section_c)

    await uow.lectures.add(lecture_1)
    await uow.lectures.add(lecture_2)
    await uow.lectures.add(lecture_3)
    await uow.lectures.add(lecture_4)

    return {
    "uow": uow,
    "actor": actor,
    "course": course,
    "module_a": module_a,
    "module_b": module_b,
    "section_a": section_a,
    "section_b": section_b,
    "section_c": section_c,
    "lecture_1": lecture_1,
    "lecture_2": lecture_2,
    "lecture_3": lecture_3,
    "lecture_4": lecture_4,
}




@pytest.mark.asyncio
async def test_delete_lecture_removes_lecture_from_tree(course_tree):
    uow = course_tree["uow"]
    section = course_tree["section_a"]
    lecture = course_tree["lecture_1"]

    use_case = DeleteLectureUseCase(uow=uow)

    await use_case.execute(
        DeleteLectureCommand(
            actor=course_tree["actor"],
            lecture_id=lecture.id,
        )
    )

    assert lecture.id not in uow.lectures.items
    assert lecture.id not in section.lecture_ids

    # Соседняя лекция осталась
    assert course_tree["lecture_2"].id in uow.lectures.items
    assert course_tree["lecture_2"].id in section.lecture_ids

    # Родители остались
    assert section.id in uow.sections.items
    assert course_tree["module_a"].id in uow.modules.items
    assert course_tree["course"].id in uow.courses.items

    assert uow.committed is True
    
    
    
    
@pytest.mark.asyncio
async def test_delete_section_removes_section_and_its_lectures(
    course_tree,
):
    uow = course_tree["uow"]
    module = course_tree["module_a"]
    section = course_tree["section_a"]

    use_case = DeleteSectionUseCase(uow=uow)

    await use_case.execute(
        DeleteSectionCommand(
            section_id=section.id,
            actor=course_tree["actor"],
        )
    )

    assert section.id not in uow.sections.items
    assert section.id not in module.section_ids

    # Lectures are deleted by cascade in , and I dont know do I need delete them here or not

    assert uow.committed is True
    
    
    
@pytest.mark.asyncio
async def test_delete_module_removes_entire_module_tree(
    course_tree,
):
    uow = course_tree["uow"]
    course = course_tree["course"]
    module = course_tree["module_a"]

    use_case = DeleteModuleUseCase(uow=uow)

    await use_case.execute(
        DeleteModuleCommand(
            module_id=module.id,
            actor=course_tree["actor"],
        )
    )
    assert module.id not in uow.modules.items
    assert module.id not in course.module_ids

    assert course_tree["section_a"].id in uow.sections.items
    assert course_tree["section_b"].id in uow.sections.items
    assert course_tree["lecture_1"].id in uow.lectures.items
    assert course_tree["lecture_2"].id in uow.lectures.items

    assert uow.committed is True
    
    
    
@pytest.mark.asyncio
async def test_delete_course_removes_entire_tree(course_tree):
    uow = course_tree["uow"]
    course = course_tree["course"]

    use_case = DeleteCourseUseCase(uow=uow)

    await use_case.execute(
        DeleteCourseCommand(
            course_id=course.id,
            actor=course_tree["actor"],
        )
    )

    assert course.id not in uow.courses.items

    assert course_tree["module_a"].id in uow.modules.items
    assert course_tree["module_b"].id in uow.modules.items

    assert course_tree["section_a"].id in uow.sections.items
    assert course_tree["section_b"].id in uow.sections.items
    assert course_tree["section_c"].id in uow.sections.items

    assert course_tree["lecture_1"].id in uow.lectures.items
    assert course_tree["lecture_2"].id in uow.lectures.items
    assert course_tree["lecture_3"].id in uow.lectures.items
    assert course_tree["lecture_4"].id in uow.lectures.items

    assert uow.committed is True
    
    
    
    
@pytest.mark.asyncio
async def test_delete_course_raises_not_found_if_course_does_not_exist():
    uow = FakeUnitOfWork()
    use_case = DeleteCourseUseCase(uow=uow)
    actor = make_author()

    with pytest.raises(CourseNotFoundError):
        await use_case.execute(
            DeleteCourseCommand(
                course_id=uuid4(),
                actor=actor,
            )
        )
    

@pytest.mark.asyncio
async def test_delete_module_raises_not_found_if_module_does_not_exist():
    uow = FakeUnitOfWork()
    use_case = DeleteModuleUseCase(uow=uow)
    actor = make_author()

    with pytest.raises(ModuleNotFoundError):
        await use_case.execute(
            DeleteModuleCommand(
                module_id=uuid4(),
                actor=actor,
            )
        )
        

@pytest.mark.asyncio
async def test_delete_section_raises_not_found_if_section_does_not_exist():
    uow = FakeUnitOfWork()
    use_case = DeleteSectionUseCase(uow=uow)
    actor = make_author()

    with pytest.raises(SectionNotFoundError):
        await use_case.execute(
            DeleteSectionCommand(
                section_id=uuid4(),
                actor=actor,
            )
        )
        
@pytest.mark.asyncio
async def test_delete_lecture_raises_not_found_if_lecture_does_not_exist():
    uow = FakeUnitOfWork()
    use_case = DeleteLectureUseCase(uow=uow)
    actor = make_author()

    with pytest.raises(LectureNotFoundError):
        await use_case.execute(
            DeleteLectureCommand(
                lecture_id=uuid4(),
                actor=actor,
            )
        )
        

from uuid import uuid4

import pytest

from app.domain.entities.course import Course, CourseStatus
from app.domain.exceptions import (
    InvalidCourseError,
    InvalidCourseStatusTransitionError,
)

def test_course_is_created_with_valid_data() -> None:
    course = Course(
        id=uuid4(),
        author_id=uuid4(),
        title='FastAPI course',
        description='Clean architecture in practice.',
    )

    assert course.title == 'FastAPI course'
    assert course.description == 'Clean architecture in practice.'
    assert course.module_ids == []


def test_course_raises_error_when_title_is_blank() -> None:
    with pytest.raises(InvalidCourseError):
        Course(
            id=uuid4(),
            author_id=uuid4(),
            title='   ',
            description='Valid description',
        )


def test_course_raises_error_when_description_is_blank() -> None:
    with pytest.raises(InvalidCourseError):
        Course(
            id=uuid4(),
            author_id=uuid4(),
            title='Valid title',
            description='   ',
        )


def test_course_update_changes_state() -> None:
    course = Course(
        id=uuid4(),
        author_id=uuid4(),
        title='Old title',
        description='Old description',
    )

    course.update(title='New title', description='New description')

    assert course.title == 'New title'
    assert course.description == 'New description'


def test_course_adds_module() -> None:
    course = Course(
        id=uuid4(),
        author_id=uuid4(),
        title="FastAPI course",
        description="Clean architecture in practice",
    )

    module_id = uuid4()

    course.add_module(module_id)

    assert course.module_ids == [module_id]
    
    



def test_course_does_not_add_duplicate_module() -> None:
    course = Course(
        id=uuid4(),
        author_id=uuid4(),
        title="FastAPI course",
        description="Clean architecture in practice",
    )

    module_id = uuid4()

    course.add_module(module_id)
    course.add_module(module_id)

    assert course.module_ids == [module_id]
    


def test_course_removes_module() -> None:
    course = Course(
        id=uuid4(),
        author_id=uuid4(),
        title="FastAPI course",
        description="Clean architecture in practice",
    )

    module_id = uuid4()

    course.add_module(module_id)
    course.remove_module(module_id)

    assert course.module_ids == []
    

def test_course_raises_error_when_removing_nonexistent_module() -> None:
    course = Course(
        id=uuid4(),
        author_id=uuid4(),
        title="FastAPI course",
        description="Clean architecture in practice",
    )

    module_id = uuid4()

    with pytest.raises(InvalidCourseError):
        course.remove_module(module_id)
    
    
def build_course() -> Course:
    return Course(
        id=uuid4(),
        author_id=uuid4(),
        title='FastAPI course',
        description='Clean architecture in practice.',
    )


def test_course_is_created_with_valid_data() -> None:
    course = build_course()

    assert course.title == 'FastAPI course'
    assert course.description == 'Clean architecture in practice.'
    assert course.status is CourseStatus.DRAFT
    assert course.module_ids == []
    assert course.is_publicly_visible() is False


def test_course_raises_error_when_title_is_blank() -> None:
    with pytest.raises(InvalidCourseError):
        Course(
            id=uuid4(),
            author_id=uuid4(),
            title='   ',
            description='Valid description',
        )


def test_course_raises_error_when_description_is_blank() -> None:
    with pytest.raises(InvalidCourseError):
        Course(
            id=uuid4(),
            author_id=uuid4(),
            title='Valid title',
            description='   ',
        )


def test_course_update_changes_state() -> None:
    course = build_course()

    course.update(title='New title', description='New description')

    assert course.title == 'New title'
    assert course.description == 'New description'


def test_draft_course_can_be_published() -> None:
    course = build_course()

    course.publish()

    assert course.status is CourseStatus.PUBLISHED
    assert course.is_publicly_visible() is True


def test_published_course_can_be_archived() -> None:
    course = build_course()
    course.publish()

    course.archive()

    assert course.status is CourseStatus.ARCHIVED
    assert course.is_publicly_visible() is False


def test_archived_course_can_be_published_again() -> None:
    course = build_course()
    course.publish()
    course.archive()

    course.publish()

    assert course.status is CourseStatus.PUBLISHED


def test_published_course_cannot_be_published_again() -> None:
    course = build_course()
    course.publish()

    with pytest.raises(InvalidCourseStatusTransitionError):
        course.publish()


def test_only_published_course_can_be_archived() -> None:
    course = build_course()

    with pytest.raises(InvalidCourseStatusTransitionError):
        course.archive()
from uuid import uuid4

import pytest

from app.domain.entities.lecture import Lecture
from app.domain.exceptions import InvalidLectureError


def test_lecture_is_created_with_valid_data() -> None:
    lecture = Lecture(
        id=uuid4(),
        section_id=uuid4(),
        title='Lecture 1',
        content='Full lecture content',
        position=1,
    )

    assert lecture.title == 'Lecture 1'
    assert lecture.content == 'Full lecture content'
    assert lecture.position == 1


def test_lecture_raises_error_when_content_is_blank() -> None:
    with pytest.raises(InvalidLectureError):
        Lecture(
            id=uuid4(),
            section_id=uuid4(),
            title='Lecture 1',
            content='   ',
            position=1,
        )


def test_lecture_update_changes_fields() -> None:
    lecture = Lecture(
        id=uuid4(),
        section_id=uuid4(),
        title='Old title',
        content='Old content',
        position=1,
    )

    lecture.update(title='New title', content='New content', position=2)

    assert lecture.title == 'New title'
    assert lecture.content == 'New content'
    assert lecture.position == 2
    
    
def test_lecture_raises_error_when_position_is_not_positive() -> None:
    with pytest.raises(InvalidLectureError):
        Lecture(
            id=uuid4(),
            section_id=uuid4(),
            title='Lecture 1',
            content='Valid content',
            position=0,
        )
        
def test_lecture_raises_error_when_title_is_blank() -> None:
    with pytest.raises(InvalidLectureError):
        Lecture(
            id=uuid4(),
            section_id=uuid4(),
            title='   ',
            content='Valid content',
            position=1,
        )
        
def test_lecture_update_raises_error_for_invalid_data() -> None:
    lecture = Lecture(
        id=uuid4(),
        section_id=uuid4(),
        title='Valid title',
        content='Valid content',
        position=1,
    )

    with pytest.raises(InvalidLectureError):
        lecture.update(title='', content='New content', position=2)

    with pytest.raises(InvalidLectureError):
        lecture.update(title='New title', content='New content', position=0)
    
    with pytest.raises(InvalidLectureError):
        lecture.update(title='New title', content='', position=2)
        


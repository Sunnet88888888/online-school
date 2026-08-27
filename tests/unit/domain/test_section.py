from uuid import uuid4

import pytest

from app.domain.entities.section import Section
from app.domain.exceptions import InvalidSectionError


def test_section_is_created_with_valid_data() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Section 1',
        description='',
        position=1,
    )

    assert section.title == 'Section 1'
    assert section.description == ''
    assert section.lecture_ids == []


def test_section_raises_error_when_title_is_blank() -> None:
    with pytest.raises(InvalidSectionError):
        Section(
            id=uuid4(),
            module_id=uuid4(),
            title='   ',
            description='Anything',
            position=1,
        )


def test_section_raises_error_when_position_is_not_positive() -> None:
    with pytest.raises(InvalidSectionError):
        Section(
            id=uuid4(),
            module_id=uuid4(),
            title='Section 1',
            description='Anything',
            position=0,
        )
        
        
        
def test_section_adds_lecture() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Section 1',
        description='',
        position=1,
    )

    lecture_id = uuid4()
    section.add_lecture(lecture_id)

    assert lecture_id in section.lecture_ids
    
    
def test_section_does_not_add_duplicate_lecture() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Section 1',
        description='',
        position=1,
    )

    lecture_id = uuid4()
    section.add_lecture(lecture_id)
    section.add_lecture(lecture_id)  # Attempt to add the same lecture again

    assert section.lecture_ids.count(lecture_id) == 1  # Ensure only one instance exists
    

def test_section_update_changes_fields() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Old title',
        description='Old description',
        position=1,
    )

    section.update(title='New title', description='New description', position=2)

    assert section.title == 'New title'
    assert section.description == 'New description'
    assert section.position == 2
    

def test_section_remove_lecture_removes_existing_lecture() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Section 1',
        description='',
        position=1,
    )

    lecture_id = uuid4()
    section.add_lecture(lecture_id)
    section.remove_lecture(lecture_id)

    assert lecture_id not in section.lecture_ids
    
    
def test_section_remove_lecture_raises_error_for_nonexistent_lecture() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Section 1',
        description='',
        position=1,
    )

    lecture_id = uuid4()

    with pytest.raises(InvalidSectionError):
        section.remove_lecture(lecture_id)
        
        
def test_section_update_raises_error_for_invalid_data() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title='Valid title',
        description='Valid description',
        position=1,
    )

    with pytest.raises(InvalidSectionError):
        section.update(title='', description='New description', position=2)

    with pytest.raises(InvalidSectionError):
        section.update(title='New title', description='New description', position=0)
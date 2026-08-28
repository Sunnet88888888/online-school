
from uuid import uuid4
import pytest

from app.infrastructure.database.models.course_model import CourseModel
from app.infrastructure.database.models.lecture_model import LectureModel
from app.infrastructure.database.models.module_model import ModuleModel
from app.infrastructure.database.models.section_model import SectionModel

from httpx import AsyncClient



@pytest.mark.asyncio
async def test_get_courses_returns_public_list(client, seeded_course_tree):
    response = await client.get('/api/courses')

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]['title'] == seeded_course_tree.course_title
    
    
    
    
    
    
    
@pytest.mark.asyncio
async def test_get_course_returns_single_course(client, seeded_course_tree):
    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.course_id
    assert payload['title'] == seeded_course_tree.course_title
    
    
    
    
    
@pytest.mark.asyncio
async def test_get_course_returns_404_when_course_is_missing(client):
    response = await client.get(f'/api/courses/{uuid4()}')

    assert response.status_code == 404
    payload = response.json()
    assert payload['error'] == 'course_not_found'
    
    
    
    
    
    
@pytest.mark.asyncio
async def test_get_course_structure_returns_modules_sections_and_lectures(client, seeded_course_tree):
    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}/structure')

    assert response.status_code == 200
    payload = response.json()
    assert payload['title'] == seeded_course_tree.course_title
    assert len(payload['modules']) == 1
    assert len(payload['modules'][0]['sections']) == 1
    assert len(payload['modules'][0]['sections'][0]['lectures']) == 1
    
    
    
    
    
    
    
    
@pytest.mark.asyncio
async def test_get_lecture_returns_full_content(client, seeded_course_tree):
    response = await client.get(f'/api/lectures/{seeded_course_tree.lecture_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.lecture_id
    assert payload['content'] == seeded_course_tree.lecture_content
    
    
    
    
@pytest.mark.asyncio
async def test_delete_lecture(
    client,
    admin_auth_headers,
    seeded_course_tree,
    session_factory,
):
    response = await client.delete(
        f"/api/admin/lectures/{seeded_course_tree.lecture_id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204

    async with session_factory() as session:
        lecture = await session.get(
            LectureModel,
            seeded_course_tree.lecture_id,
        )
        section: SectionModel = await session.get(
            SectionModel,
            seeded_course_tree.section_id,
        )

    assert lecture is None





@pytest.mark.asyncio
async def test_delete_section_cascades_lectures(
    client: AsyncClient,
    admin_auth_headers,
    seeded_course_tree,
    session_factory,
):
    response = await client.delete(
        f"/api/admin/sections/{seeded_course_tree.section_id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204

    async with session_factory() as session:
        section = await session.get(
            SectionModel,
            seeded_course_tree.section_id,
        )
        lecture = await session.get(
            LectureModel,
            seeded_course_tree.lecture_id,
        )
        module = await session.get(
            ModuleModel,
            seeded_course_tree.module_id,
        )

    assert section is None
    assert lecture is None
    assert module is not None
    
    
    
    
    
@pytest.mark.asyncio
async def test_delete_module_cascades_sections_and_lectures(
    client:AsyncClient,
    admin_auth_headers,
    seeded_course_tree,
    session_factory,
):
    response = await client.delete(
        f"/api/admin/modules/{seeded_course_tree.module_id}",
        headers=admin_auth_headers,
    ) 

    assert response.status_code == 204

    async with session_factory() as session:
        module = await session.get(
            ModuleModel,
            seeded_course_tree.module_id,
        )
        section = await session.get(
            SectionModel,
            seeded_course_tree.section_id,
        )
        lecture = await session.get(
            LectureModel,
            seeded_course_tree.lecture_id,
        )

    assert module is None
    assert section is None
    assert lecture is None
    
    
    
@pytest.mark.asyncio
async def test_delete_course_cascades_modules_sections_and_lectures(
    client: AsyncClient,
    admin_auth_headers,
    seeded_course_tree,
    session_factory,
):
    response = await client.delete(
        f"/api/admin/courses/{seeded_course_tree.course_id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204

    async with session_factory() as session:
        course = await session.get(
            CourseModel,
            seeded_course_tree.course_id,
        )
        module = await session.get(
            ModuleModel,
            seeded_course_tree.module_id,
        )
        section = await session.get(
            SectionModel,
            seeded_course_tree.section_id,
        )
        lecture = await session.get(
            LectureModel,
            seeded_course_tree.lecture_id,
        )

    assert course is None
    assert module is None
    assert section is None
    assert lecture is None
    
    
    
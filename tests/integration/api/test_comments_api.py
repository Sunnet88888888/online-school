from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.infrastructure.database.models import CourseModel


def normalize_iso_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    normalized = value.replace('Z', '+00:00')
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


async def get_current_user_id(client, headers):
    response = await client.get('/api/auth/me', headers=headers)
    assert response.status_code == 200
    return response.json()['id']


async def create_comment(client, headers, target_type, target_id, text='Useful question.'):
    return await client.post(
        f'/api/comments/{target_type}/{target_id}',
        headers=headers,
        json={'text': text},
    )


async def list_comments(client, headers, target_type, target_id):
    return await client.get(
        f'/api/comments/{target_type}/{target_id}',
        headers=headers,
    )


@pytest.mark.asyncio
async def test_student_can_create_comment_for_lecture_target(
    client,
    student_auth_headers,
    seeded_course_tree,
):
    user_id = await get_current_user_id(client, student_auth_headers)

    response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Text for supported target type.',
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['user_id'] == user_id
    assert payload['text'] == 'Text for supported target type.'
    assert payload['id']
    assert payload['created_at']
    assert payload['updated_at'] is None

    get_response = await list_comments(client, student_auth_headers, 'lecture', seeded_course_tree.lecture_id)
    assert get_response.status_code == 200
    assert any(item['id'] == payload['id'] for item in get_response.json())


@pytest.mark.asyncio
async def test_student_can_create_comment_for_task_target(
    client,
    student_auth_headers,
    seeded_tasks_tree,
):
    user_id = await get_current_user_id(client, student_auth_headers)

    response = await create_comment(
        client,
        student_auth_headers,
        'task',
        seeded_tasks_tree.task_id,
        text='Text for task target.',
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['user_id'] == user_id
    assert payload['text'] == 'Text for task target.'


@pytest.mark.asyncio
async def test_student_can_create_comment_for_code_task_target(
    client,
    student_auth_headers,
    seeded_tasks_tree,
):
    user_id = await get_current_user_id(client, student_auth_headers)

    response = await create_comment(
        client,
        student_auth_headers,
        'code_task',
        seeded_tasks_tree.code_task_id,
        text='Text for code task target.',
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['user_id'] == user_id
    assert payload['text'] == 'Text for code task target.'


@pytest.mark.asyncio
async def test_student_can_create_comment_for_question_target(
    client,
    student_auth_headers,
    seeded_interactive_tree,
):
    user_id = await get_current_user_id(client, student_auth_headers)

    response = await create_comment(
        client,
        student_auth_headers,
        'question',
        seeded_interactive_tree.question_id,
        text='Text for question target.',
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['user_id'] == user_id
    assert payload['text'] == 'Text for question target.'


@pytest.mark.asyncio
async def test_author_can_create_comment_in_own_course(
    client,
    author_auth_headers,
    seeded_tasks_tree,
):
    current_user_id = await get_current_user_id(client, author_auth_headers)

    response = await create_comment(
        client,
        author_auth_headers,
        'task',
        seeded_tasks_tree.task_id,
        text='Author comment on own course.',
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['user_id'] == current_user_id
    assert payload['text'] == 'Author comment on own course.'


@pytest.mark.asyncio
async def test_admin_can_create_comment(
    client,
    admin_auth_headers,
    seeded_course_tree,
):
    current_user_id = await get_current_user_id(client, admin_auth_headers)

    response = await create_comment(
        client,
        admin_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Admin comment on public lecture.',
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['user_id'] == current_user_id
    assert payload['text'] == 'Admin comment on public lecture.'


@pytest.mark.asyncio
async def test_create_comment_requires_auth(client, seeded_course_tree):
    response = await create_comment(
        client,
        {},
        'lecture',
        seeded_course_tree.lecture_id,
        text='No auth header',
    )

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'


@pytest.mark.asyncio
async def test_create_comment_rejects_draft_course_for_student(
    client,
    student_auth_headers,
    seeded_course_tree,
    session_factory,
):
    async with session_factory() as session:
        course = await session.get(CourseModel, seeded_course_tree.course_id)
        assert course is not None
        course.status = 'draft'
        await session.commit()

    response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Student should not comment here.',
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_create_comment_rejects_missing_target(client, student_auth_headers):
    response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        str(uuid4()),
        text='Missing lecture.',
    )

    assert response.status_code == 404
    assert response.json()['error'] == 'lecture_not_found'


@pytest.mark.asyncio
async def test_create_comment_rejects_invalid_target_type(client, student_auth_headers):
    response = await client.post(
        f"/api/comments/invalid/{uuid4()}",
        headers=student_auth_headers,
        json={'text': 'Bad target type.'},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_comment_rejects_invalid_text(client, student_auth_headers, seeded_course_tree):
    response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='',
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_student_can_get_comments_for_lecture_target(
    client,
    student_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Visible comment on target.',
    )
    assert create_response.status_code == 201

    response = await list_comments(client, student_auth_headers, 'lecture', seeded_course_tree.lecture_id)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 1
    assert any(item['text'] == 'Visible comment on target.' for item in payload)


@pytest.mark.asyncio
async def test_student_can_get_comments_for_task_target(
    client,
    student_auth_headers,
    seeded_tasks_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'task',
        seeded_tasks_tree.task_id,
        text='Visible task comment.',
    )
    assert create_response.status_code == 201

    response = await list_comments(client, student_auth_headers, 'task', seeded_tasks_tree.task_id)

    assert response.status_code == 200
    payload = response.json()
    assert any(item['text'] == 'Visible task comment.' for item in payload)


@pytest.mark.asyncio
async def test_student_can_get_comments_for_code_task_target(
    client,
    student_auth_headers,
    seeded_tasks_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'code_task',
        seeded_tasks_tree.code_task_id,
        text='Visible code task comment.',
    )
    assert create_response.status_code == 201

    response = await list_comments(client, student_auth_headers, 'code_task', seeded_tasks_tree.code_task_id)

    assert response.status_code == 200
    payload = response.json()
    assert any(item['text'] == 'Visible code task comment.' for item in payload)


@pytest.mark.asyncio
async def test_student_can_get_comments_for_question_target(
    client,
    student_auth_headers,
    seeded_interactive_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'question',
        seeded_interactive_tree.question_id,
        text='Visible question comment.',
    )
    assert create_response.status_code == 201

    response = await list_comments(client, student_auth_headers, 'question', seeded_interactive_tree.question_id)

    assert response.status_code == 200
    payload = response.json()
    assert any(item['text'] == 'Visible question comment.' for item in payload)


@pytest.mark.asyncio
async def test_unauthenticated_user_cannot_get_comments_without_auth(
    client,
    student_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Public comment for anonymous reader.',
    )
    assert create_response.status_code == 201

    response = await list_comments(client, {}, 'lecture', seeded_course_tree.lecture_id)

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'


@pytest.mark.asyncio
async def test_user_without_access_cannot_get_comments_for_draft_course(
    client,
    student_auth_headers,
    seeded_course_tree,
    session_factory,
):
    async with session_factory() as session:
        course = await session.get(CourseModel, seeded_course_tree.course_id)
        assert course is not None
        course.status = 'draft'
        await session.commit()

    response = await list_comments(client, student_auth_headers, 'lecture', seeded_course_tree.lecture_id)

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_get_comments_rejects_missing_target(client, student_auth_headers):
    response = await list_comments(client, student_auth_headers, 'lecture', str(uuid4()))

    assert response.status_code == 404
    assert response.json()['error'] == 'lecture_not_found'


@pytest.mark.asyncio
async def test_get_comments_does_not_include_other_targets(
    client,
    student_auth_headers,
    seeded_course_tree,
    seeded_tasks_tree,
):
    lecture_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Only lecture comment.',
    )
    assert lecture_response.status_code == 201

    task_response = await client.get(
        f'/api/comments/task/{seeded_tasks_tree.task_id}',
        headers=student_auth_headers,
    )

    assert task_response.status_code == 200
    payload = task_response.json()
    assert all(item['text'] != 'Only lecture comment.' for item in payload)


@pytest.mark.asyncio
async def test_student_can_update_own_comment(client, student_auth_headers, seeded_course_tree):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Original text.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']
    created_at = create_response.json()['created_at']
    user_id = await get_current_user_id(client, student_auth_headers)

    update_response = await client.put(
        f'/api/comments/{comment_id}',
        headers=student_auth_headers,
        json={'text': 'Updated text.'},
    )

    assert update_response.status_code == 200
    payload = update_response.json()
    assert payload['id'] == comment_id
    assert payload['user_id'] == user_id
    assert payload['text'] == 'Updated text.'
    assert normalize_iso_datetime(payload['created_at']) == normalize_iso_datetime(created_at)
    assert payload['updated_at'] is not None

    get_response = await client.get(
        f'/api/comments/lecture/{seeded_course_tree.lecture_id}',
        headers=student_auth_headers,
    )
    assert get_response.status_code == 200
    assert any(item['id'] == comment_id and item['text'] == 'Updated text.' for item in get_response.json())


@pytest.mark.asyncio
async def test_student_cannot_update_other_users_comment(
    client,
    student_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Original owner comment.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    register_response = await client.post(
        '/api/auth/register',
        json={'email': 'second-student@example.com', 'password': 'strongpassword123'},
    )
    assert register_response.status_code == 201

    second_login = await client.post(
        '/api/auth/login',
        json={'email': 'second-student@example.com', 'password': 'strongpassword123'},
    )
    second_headers = {'Authorization': f"Bearer {second_login.json()['access_token']}"}

    response = await client.put(
        f'/api/comments/{comment_id}',
        headers=second_headers,
        json={'text': 'Not allowed.'},
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_author_cannot_update_other_users_comment_even_in_own_course(
    client,
    author_auth_headers,
    student_auth_headers,
    seeded_tasks_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'task',
        seeded_tasks_tree.task_id,
        text='Owned by student on author course.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    response = await client.put(
        f'/api/comments/{comment_id}',
        headers=author_auth_headers,
        json={'text': 'Author update attempt.'},
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_admin_can_update_other_users_comment(
    client,
    student_auth_headers,
    admin_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Student comment before admin update.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    response = await client.put(
        f'/api/comments/{comment_id}',
        headers=admin_auth_headers,
        json={'text': 'Admin update applied.'},
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_student_can_delete_own_comment(client, student_auth_headers, seeded_course_tree):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Comment to delete.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    delete_response = await client.delete(
        f'/api/comments/{comment_id}',
        headers=student_auth_headers,
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b''

    get_response = await list_comments(client, student_auth_headers, 'lecture', seeded_course_tree.lecture_id)
    assert get_response.status_code == 200
    assert all(item['id'] != comment_id for item in get_response.json())


@pytest.mark.asyncio
async def test_student_cannot_delete_other_users_comment(
    client,
    student_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Someone else comment.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    register_response = await client.post(
        '/api/auth/register',
        json={'email': 'third-student@example.com', 'password': 'strongpassword123'},
    )
    assert register_response.status_code == 201

    second_login = await client.post(
        '/api/auth/login',
        json={'email': 'third-student@example.com', 'password': 'strongpassword123'},
    )
    second_headers = {'Authorization': f"Bearer {second_login.json()['access_token']}"}

    response = await client.delete(
        f'/api/comments/{comment_id}',
        headers=second_headers,
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_author_can_delete_other_users_comment_in_own_course(
    client,
    student_auth_headers,
    author_auth_headers,
    seeded_tasks_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'task',
        seeded_tasks_tree.task_id,
        text='Comment on author course.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    response = await client.delete(
        f'/api/comments/{comment_id}',
        headers=author_auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_author_cannot_delete_comment_from_other_course(
    client,
    student_auth_headers,
    author_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Comment from different course.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    response = await client.delete(
        f'/api/comments/{comment_id}',
        headers=author_auth_headers,
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_admin_can_delete_other_users_comment(
    client,
    student_auth_headers,
    admin_auth_headers,
    seeded_course_tree,
):
    create_response = await create_comment(
        client,
        student_auth_headers,
        'lecture',
        seeded_course_tree.lecture_id,
        text='Comment admin deletes.',
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()['id']

    response = await client.delete(
        f'/api/comments/{comment_id}',
        headers=admin_auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_missing_comment_returns_400(client, admin_auth_headers):
    response = await client.delete(
        f'/api/comments/{uuid4()}',
        headers=admin_auth_headers,
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'application_error'

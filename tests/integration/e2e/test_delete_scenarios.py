from sqlalchemy import select

import pytest

from app.infrastructure.database.models import (
    CodeSubmissionModel,
    CodeTaskModel,
    TaskAttemptModel,
    TestCaseModel,
)
import app.presentation.api.dependencies as api_dependencies


class FakeSubmissionQueue:
    def __init__(self) -> None:
        self.items = []

    async def enqueue(self, submission_id) -> None:
        self.items.append(submission_id)


@pytest.fixture
def fake_submission_queue(monkeypatch):
    queue = FakeSubmissionQueue()
    monkeypatch.setattr(
        api_dependencies,
        'build_submission_queue',
        lambda: queue,
    )
    return queue


@pytest.mark.asyncio
async def test_author_can_delete_task_and_it_disappears_from_course_structure(
    client,
    author_auth_headers,
):
    course_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={'title': 'Delete task course', 'description': 'Course to delete task from.'},
    )
    course_id = course_response.json()['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=author_auth_headers,
        json={'title': 'Tasks', 'description': 'Practice', 'position': 1},
    )
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=author_auth_headers,
        json={'title': 'Basics', 'description': 'Intro', 'position': 1},
    )
    section_id = section_response.json()['id']

    task_response = await client.post(
        f'/api/admin/sections/{section_id}/tasks',
        headers=author_auth_headers,
        json={
            'title': 'HTTP method',
            'statement': 'Enter GET.',
            'position': 1,
            'check_type': 'exact_match',
            'expected_answer': 'GET',
            'accepted_answers': [],
            'answer_pattern': '',
            'max_attempts': 2,
            'reward_points': 3,
        },
    )
    task_id = task_response.json()['id']

    delete_response = await client.delete(
        f'/api/admin/tasks/{task_id}',
        headers=author_auth_headers,
    )

    assert delete_response.status_code == 204

    structure_response = await client.get(
        f'/api/courses/{course_id}/structure',
        headers=author_auth_headers,
    )
    section = structure_response.json()['modules'][0]['sections'][0]
    assert task_id not in section['task_ids']
    assert all(item['id'] != task_id for item in section['tasks'])


@pytest.mark.asyncio
async def test_author_can_delete_code_task_and_it_disappears_from_course_structure(
    client,
    author_auth_headers,
):
    course_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={'title': 'Delete code task course', 'description': 'Course to delete code task from.'},
    )
    course_id = course_response.json()['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=author_auth_headers,
        json={'title': 'Python', 'description': 'Practice', 'position': 1},
    )
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=author_auth_headers,
        json={'title': 'Code basics', 'description': 'Intro', 'position': 1},
    )
    section_id = section_response.json()['id']

    code_task_response = await client.post(
        f'/api/admin/sections/{section_id}/code-tasks',
        headers=author_auth_headers,
        json={
            'title': 'Sum numbers',
            'statement': 'Read two integers and print their sum.',
            'position': 1,
            'language': 'python',
            'starter_code': 'a, b = map(int, input().split())',
            'max_attempts': 2,
            'reward_points': 5,
            'time_limit_seconds': 20,
            'memory_limit_mb': 128,
        },
    )
    code_task_id = code_task_response.json()['id']

    delete_response = await client.delete(
        f'/api/admin/code-tasks/{code_task_id}',
        headers=author_auth_headers,
    )

    assert delete_response.status_code == 204

    structure_response = await client.get(
        f'/api/courses/{course_id}/structure',
        headers=author_auth_headers,
    )
    section = structure_response.json()['modules'][0]['sections'][0]
    assert code_task_id not in section['code_task_ids']
    assert all(item['id'] != code_task_id for item in section['code_tasks'])


@pytest.mark.asyncio
async def test_author_cannot_delete_used_task_and_history_is_preserved(
    client,
    author_auth_headers,
    student_auth_headers,
    session_factory,
):
    course_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={'title': 'Used task course', 'description': 'Course with task attempts.'},
    )
    course_id = course_response.json()['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=author_auth_headers,
        json={'title': 'Practice', 'description': 'Tasks', 'position': 1},
    )
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=author_auth_headers,
        json={'title': 'Task section', 'description': 'Intro', 'position': 1},
    )
    section_id = section_response.json()['id']

    task_response = await client.post(
        f'/api/admin/sections/{section_id}/tasks',
        headers=author_auth_headers,
        json={
            'title': 'HTTP method',
            'statement': 'Enter GET.',
            'position': 1,
            'check_type': 'exact_match',
            'expected_answer': 'GET',
            'accepted_answers': [],
            'answer_pattern': '',
            'max_attempts': 2,
            'reward_points': 3,
        },
    )
    task_id = task_response.json()['id']

    attempt_response = await client.post(
        f'/api/learning/tasks/{task_id}/attempts',
        headers=student_auth_headers,
        json={'submitted_answer': 'GET'},
    )
    assert attempt_response.status_code == 201

    delete_response = await client.delete(
        f'/api/admin/tasks/{task_id}',
        headers=author_auth_headers,
    )

    assert delete_response.status_code == 400
    payload = delete_response.json()
    assert payload['error'] == 'application_error'

    async with session_factory() as session:
        attempts = (await session.execute(select(TaskAttemptModel))).scalars().all()

    assert len(attempts) == 1
    assert attempts[0].task_id == task_id

    structure_response = await client.get(
        f'/api/courses/{course_id}/structure',
        headers=author_auth_headers,
    )
    section = structure_response.json()['modules'][0]['sections'][0]
    assert task_id in section['task_ids']


@pytest.mark.asyncio
async def test_author_cannot_delete_used_code_task_and_history_is_preserved(
    client,
    author_auth_headers,
    student_auth_headers,
    session_factory,
    fake_submission_queue,
):
    course_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={'title': 'Used code task course', 'description': 'Course with code submissions.'},
    )
    course_id = course_response.json()['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=author_auth_headers,
        json={'title': 'Python', 'description': 'Practice', 'position': 1},
    )
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=author_auth_headers,
        json={'title': 'Code section', 'description': 'Intro', 'position': 1},
    )
    section_id = section_response.json()['id']

    code_task_response = await client.post(
        f'/api/admin/sections/{section_id}/code-tasks',
        headers=author_auth_headers,
        json={
            'title': 'Sum numbers',
            'statement': 'Read two integers and print their sum.',
            'position': 1,
            'language': 'python',
            'starter_code': 'a, b = map(int, input().split())',
            'max_attempts': 2,
            'reward_points': 5,
            'time_limit_seconds': 20,
            'memory_limit_mb': 128,
        },
    )
    code_task_id = code_task_response.json()['id']

    create_test_case_response = await client.post(
        f'/api/admin/code-tasks/{code_task_id}/test-cases',
        headers=author_auth_headers,
        json={
            'position': 1,
            'input_data': '2 3',
            'expected_output': '5',
            'is_hidden': False,
            'explanation': 'basic case',
        },
    )
    assert create_test_case_response.status_code == 201

    submission_response = await client.post(
        f'/api/learning/code-tasks/{code_task_id}/submissions',
        headers=student_auth_headers,
        json={'source_code': 'a, b = map(int, input().split())\nprint(a + b)'},
    )
    assert submission_response.status_code == 202
    submission_id = submission_response.json()['id']
    assert submission_id is not None

    delete_response = await client.delete(
        f'/api/admin/code-tasks/{code_task_id}',
        headers=author_auth_headers,
    )

    assert delete_response.status_code == 400
    payload = delete_response.json()
    assert payload['error'] == 'application_error'

    async with session_factory() as session:
        submissions = (await session.execute(select(CodeSubmissionModel))).scalars().all()

    assert len(submissions) == 1
    assert submissions[0].id == submission_id

    structure_response = await client.get(
        f'/api/courses/{course_id}/structure',
        headers=author_auth_headers,
    )
    section = structure_response.json()['modules'][0]['sections'][0]
    assert code_task_id in section['code_task_ids']


@pytest.mark.asyncio
async def test_author_can_delete_one_test_case_before_submission_and_delete_is_blocked_after_submission(
    client,
    author_auth_headers,
    student_auth_headers,
    session_factory,
    fake_submission_queue,
):
    course_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={'title': 'Delete test case course', 'description': 'Course with code task test cases.'},
    )
    course_id = course_response.json()['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=author_auth_headers,
        json={'title': 'Python', 'description': 'Practice', 'position': 1},
    )
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=author_auth_headers,
        json={'title': 'Test cases', 'description': 'Intro', 'position': 1},
    )
    section_id = section_response.json()['id']

    code_task_response = await client.post(
        f'/api/admin/sections/{section_id}/code-tasks',
        headers=author_auth_headers,
        json={
            'title': 'Sum numbers',
            'statement': 'Read two integers and print their sum.',
            'position': 1,
            'language': 'python',
            'starter_code': 'a, b = map(int, input().split())',
            'max_attempts': 2,
            'reward_points': 5,
            'time_limit_seconds': 20,
            'memory_limit_mb': 128,
        },
    )
    code_task_id = code_task_response.json()['id']

    first_case_response = await client.post(
        f'/api/admin/code-tasks/{code_task_id}/test-cases',
        headers=author_auth_headers,
        json={
            'position': 1,
            'input_data': '2 3',
            'expected_output': '5',
            'is_hidden': False,
            'explanation': 'basic case',
        },
    )
    first_case_id = first_case_response.json()['id']

    second_case_response = await client.post(
        f'/api/admin/code-tasks/{code_task_id}/test-cases',
        headers=author_auth_headers,
        json={
            'position': 2,
            'input_data': '10 20',
            'expected_output': '30',
            'is_hidden': False,
            'explanation': 'second basic case',
        },
    )
    second_case_id = second_case_response.json()['id']

    delete_case_response = await client.delete(
        f'/api/admin/test-cases/{first_case_id}',
        headers=author_auth_headers,
    )
    assert delete_case_response.status_code == 204

    async with session_factory() as session:
        remaining_cases = (await session.execute(
            select(TestCaseModel).where(TestCaseModel.code_task_id == code_task_id)
        )).scalars().all()

    assert len(remaining_cases) == 1
    assert remaining_cases[0].id == second_case_id

    submission_response = await client.post(
        f'/api/learning/code-tasks/{code_task_id}/submissions',
        headers=student_auth_headers,
        json={'source_code': 'a, b = map(int, input().split())\nprint(a + b)'},
    )
    assert submission_response.status_code == 202

    delete_second_response = await client.delete(
        f'/api/admin/test-cases/{second_case_id}',
        headers=author_auth_headers,
    )

    assert delete_second_response.status_code == 400
    payload = delete_second_response.json()
    assert payload['error'] == 'application_error'

    async with session_factory() as session:
        after_submission_cases = (await session.execute(
            select(TestCaseModel).where(TestCaseModel.code_task_id == code_task_id)
        )).scalars().all()
        submissions = (await session.execute(select(CodeSubmissionModel))).scalars().all()

    assert len(after_submission_cases) == 1
    assert len(submissions) == 1

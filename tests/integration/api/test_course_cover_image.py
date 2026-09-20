from pathlib import Path

import pytest


TEST_FILES_DIR = Path(__file__).resolve().parents[2] / 'files_for_testing'


@pytest.mark.asyncio
async def test_upload_cover_accepts_supported_image_file(client, author_auth_headers):
    create_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={
            'title': 'Course with cover',
            'description': 'Course for cover upload.',
        },
    )
    assert create_response.status_code == 201
    course_id = create_response.json()['id']

    file_path = TEST_FILES_DIR / 'supported_image.png'
    with file_path.open('rb') as fh:
        upload_response = await client.post(
            f'/api/admin/courses/{course_id}/cover',
            headers=author_auth_headers,
            files={'file': ('supported_image.png', fh.read(), 'image/png')},
        )

    assert upload_response.status_code == 200
    payload = upload_response.json()
    assert payload['id'] == course_id
    assert payload['cover_image_url'] is not None
    assert payload['cover_image_url'].startswith('/media/')
    assert payload['cover_image_url'].endswith('.png')


@pytest.mark.asyncio
async def test_upload_cover_rejects_large_video_file(client, author_auth_headers):
    create_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={
            'title': 'Big file course',
            'description': 'Large file should be rejected.',
        },
    )
    assert create_response.status_code == 201
    course_id = create_response.json()['id']

    file_path = TEST_FILES_DIR / 'big_file.mp4'
    with file_path.open('rb') as fh:
        upload_response = await client.post(
            f'/api/admin/courses/{course_id}/cover',
            headers=author_auth_headers,
            files={'file': ('big_file.mp4', fh.read(), 'video/mp4')},
        )

    assert upload_response.status_code == 413
    assert 'too large' in upload_response.json()['detail'].lower()


@pytest.mark.asyncio
async def test_upload_cover_rejects_fake_png_image(client, author_auth_headers):
    create_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={
            'title': 'Fake png course',
            'description': 'Fake png should fail content validation.',
        },
    )
    assert create_response.status_code == 201
    course_id = create_response.json()['id']

    file_path = TEST_FILES_DIR / 'fake_png_file.png'
    with file_path.open('rb') as fh:
        upload_response = await client.post(
            f'/api/admin/courses/{course_id}/cover',
            headers=author_auth_headers,
            files={'file': ('fake_png_file.png', fh.read(), 'image/png')},
        )

    assert upload_response.status_code == 400
    assert upload_response.json()['error'] == 'application_error'


@pytest.mark.asyncio
async def test_upload_cover_rejects_unsupported_extension(client, author_auth_headers):
    create_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={
            'title': 'Unsupported extension course',
            'description': 'Unsupported extension should fail validation.',
        },
    )
    assert create_response.status_code == 201
    course_id = create_response.json()['id']

    file_path = TEST_FILES_DIR / 'unsupported_file.docx'
    with file_path.open('rb') as fh:
        upload_response = await client.post(
            f'/api/admin/courses/{course_id}/cover',
            headers=author_auth_headers,
            files={'file': ('unsupported_file.docx', fh.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
        )

    assert upload_response.status_code == 400
    assert upload_response.json()['error'] == 'application_error'

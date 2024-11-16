from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse

from news.models import News


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture(
            'author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('delete_url'),
         pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('detail_url'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('home_url'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('login_url'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('logout_url'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('signup_url'),
         pytest.lazy_fixture('client'), HTTPStatus.OK),
    ),
)
def test_pages_availability_for_users(
    parametrized_client, name, expected_status,
):
    url = name
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_redirects(client, name, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.pk,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


# 11 tests

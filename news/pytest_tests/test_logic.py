from http import HTTPStatus
import pytest
from pytest_django.asserts import assertFormError

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_user_can_create_note(author_client, form_data, detail_url):
    url = detail_url
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == form_data['text']


def test_anonymous_user_cant_create_note(client, form_data, detail_url):
    url = detail_url
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(author_client, detail_url):
    url = detail_url
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    assert Comment.objects.count() == 1
    author_client.delete(url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    assert Comment.objects.count() == 1
    author_client.post(url, form_data)
    assert Comment.objects.count() == 1
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.pk,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_other_user_cant_delete_comment(not_author_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1

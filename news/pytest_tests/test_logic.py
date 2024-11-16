from http import HTTPStatus
from pytest_django.asserts import assertFormError

import pytest
from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING
from news.pytest_tests.constants import FORM_DATA


def test_user_can_create_comment(author_client, detail_url):
    comment = Comment.objects.all()
    comment.delete()
    url = detail_url
    author_client.post(url, data=FORM_DATA)
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == FORM_DATA['text']


def test_anonymous_user_cant_create_comment(client, detail_url):
    url = detail_url
    comment_count = Comment.objects.count()
    client.post(url, data=FORM_DATA)
    assert Comment.objects.count() == comment_count


def test_user_cant_use_bad_words(author_client, detail_url):
    url = detail_url
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    comment_count = Comment.objects.count()
    response = author_client.post(url, data=bad_words_data)
    assert Comment.objects.count() == comment_count
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    


def test_author_can_delete_comment(author_client, delete_url):
    url = delete_url
    comment_count = Comment.objects.count()
    author_client.delete(url)
    assert Comment.objects.count() == comment_count - 1


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment, author):
    url = reverse('news:edit', args=(comment.pk,))
    comment_count = Comment.objects.count()
    author_client.post(url, FORM_DATA)
    assert Comment.objects.count() == comment_count
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == author
    assert comment_from_db.news == comment.news


def test_other_user_cant_edit_comment(not_author_client, comment, author):
    url = reverse('news:edit', args=(comment.pk,))
    response = not_author_client.post(url, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == author
    assert comment_from_db.news == comment.news


def test_other_user_cant_delete_comment(not_author_client, delete_url):
    url = delete_url
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1

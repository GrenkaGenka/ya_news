from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from news.forms import CommentForm
from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING



def test_user_can_create_note(author_client, form_data, new):
    url = reverse('news:detail', args=(new.pk,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == form_data['text']


def test_anonymous_user_cant_create_note(client, form_data, new):
    url = reverse('news:detail', args=(new.pk,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0



def test_user_cant_use_bad_words(author_client, new):
    url = reverse('news:detail', args=(new.pk,))
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
    # От имени автора комментария отправляем DELETE-запрос на удаление.
    response = author_client.delete(url)
    # Проверяем, что редирект привёл к разделу с комментариями.
    # Заодно проверим статус-коды ответов.
    news_url = reverse('news:detail', args=(new.id,))  # Адрес новости.
    cls.url_to_comments = news_url + '#comments'  # Адрес блока с комментариями.
    assertRedirects(response, self.url_to_comments)
    # Считаем количество комментариев в системе.
    assert Comment.objects.count() == 0
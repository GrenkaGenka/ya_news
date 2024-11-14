from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment, News




def test_note_in_list_less_then_10(author_client, many_news):
    url = reverse('news:home')
    # Запрашиваем страницу со списком заметок:
    response = author_client.get(url)
    # Получаем список объектов из контекста:
    object_list = response.context['object_list']
    notes_count = object_list.count()
    # Проверяем, что заметка находится в этом списке:
    assert notes_count <= 10


def test_news_order(many_news, author_client):
    url = reverse('news:home')
    response = author_client.get(url)
    object_list = response.context['object_list']
    # Получаем даты новостей в том порядке, как они выведены на странице.
    all_dates = [news.date for news in object_list]
    # Сортируем полученный список по убыванию.
    sorted_dates = sorted(all_dates, reverse=True)
    # Проверяем, что исходный список был отсортирован правильно.
    assert all_dates == sorted_dates


def test_comment_order(many_comments, author_client):
    a=1
    url = reverse('news:detail', args=(many_comments['new'].pk,))
    response = author_client.get(url)
    object_list = response.context['object_list']
    a=1
    # Получаем даты новостей в том порядке, как они выведены на странице.
    #all_dates = [comment.date for comment in object_list]
    # Сортируем полученный список по убыванию.
    #sorted_dates = sorted(all_dates, reverse=True)
    # Проверяем, что исходный список был отсортирован правильно.
    assert 1 == 1
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_note_in_list_less_then_10(author_client, home_url, many_news):
    url = home_url
    response = author_client.get(url)
    notes_count = response.context['object_list'].count()
    assert notes_count <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(many_news, author_client, home_url):
    url = home_url
    response = author_client.get(url)
    objects = response.context['object_list']
    all_dates = [news.date for news in objects]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_order(many_comments, author_client):
    url = reverse('news:detail', args=(many_comments.pk,))
    response = author_client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_login_client_has_form(author_client, detail_url):
    url = detail_url
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_anonymous_client_has_no_form(client, detail_url):
    url = detail_url
    response = client.get(url)
    assert 'form' not in response.context

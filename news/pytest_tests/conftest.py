from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def new(author):
    new = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=timezone.now()

    )
    return new


@pytest.fixture
def comment(author, new):
    com = Comment.objects.create(
        news=new,
        author=author,
        text='Текст комментария'
    )
    return com


@pytest.fixture
def many_news(author):
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text=f'Просто текст {index}',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def many_comments(author, new):
    today = datetime.today()
    all_comment = [
        Comment(
            news=new,
            author=author,
            text=f'Текст {index}',
        )
        for index in range(11)
    ]
    Comment.objects.bulk_create(all_comment)
    return new


@pytest.fixture
def detail_url(new):
    return reverse('news:detail', args=(new.pk,))

@pytest.fixture
def home_url(new):
    return reverse('news:home')

@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))

@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login')

@pytest.fixture
def logout_url():
    return reverse('users:logout')

@pytest.fixture
def signup_url():
    return reverse('users:signup')





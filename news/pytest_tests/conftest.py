# conftest.py
import pytest

# Импортируем класс клиента.
from django.test.client import Client
from django.utils import timezone
from datetime import datetime, timedelta
# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import Comment, News


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def new(author):
    new = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст новости',
        date = timezone.now()
        
    )
    return new



@pytest.fixture
def comment(author, new):
    #new = News.objects.get()
    com = Comment.objects.create(  # Создаём объект заметки.
        news=new,
        author=author,
        text='Текст'
    )
    #news=cls.news, author=cls.author, text=f'Tекст {index}',
    return com

@pytest.fixture
def many_news(author):
    today = datetime.today()
    all_news = [        
        News(
            title=f'Новость {index}',
            text=f'Просто текст {index}',
            # Для каждой новости уменьшаем дату на index дней от today,
            # где index - счётчик цикла.
            date=today - timedelta(days=index)
        )
        for index in range(11)
        ]
    News.objects.bulk_create(all_news)
    return all_news



@pytest.fixture
def many_comments(author, new):
    today = datetime.today()
    all_comment = [
        Comment(
            news=new,
            author=author,
            text=f'Текст {index}',
            created=today - timedelta(days=index),
        )
        for index in range(11)
        ]
    Comment.objects.bulk_create(all_comment)
    #return all_comment
    all = {'all_comment': all_comment, 'new': new}
    #all = ['new'] = new
    return all

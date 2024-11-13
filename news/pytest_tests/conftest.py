# conftest.py
import pytest

# Импортируем класс клиента.
from django.test.client import Client
from django.utils import timezone
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

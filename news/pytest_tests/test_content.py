from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment, News
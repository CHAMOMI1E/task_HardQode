
from django.urls import path
from .views import *

urlpatterns = [
    path('', get_lessons_by_user_and_product, name='get_lessons_by_user_and_product'),
]

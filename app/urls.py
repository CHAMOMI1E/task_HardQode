from django.urls import path
from .views import *

urlpatterns = [
    path('/', main, name='main'),
    path('lessons/', lesson_list, name='lesson-list'),

    path('product/<int:product_id>/lessons/', product_lesson_list, name='product-lesson-list'),

    path('product/statistics/', product_statistics, name='product-statistics'),

    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('lessons/', lesson_list, name='lesson-list'),

    path('product/<int:product_id>/lessons/', product_lesson_list, name='product-lesson-list'),

    path('product/statistics/', product_statistics, name='product-statistics'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
]

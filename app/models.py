from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productc = models.ForeignKey(Product, on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    link_to_video = models.URLField()
    duration = models.IntegerField()  # Длительность в секундах
    products = models.ManyToManyField(Product)


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewing_time = models.IntegerField()  # Время просмотра в секундах
    status = models.CharField(max_length=20,
                              choices=[('Просмотрено', 'Просмотрено'), ('Не просмотрено', 'Не просмотрено')])

# Create your models here.

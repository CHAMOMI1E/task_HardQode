from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    list_display_links = ('id', 'name')


admin.site.register(Product, ProductAdmin)


class ProductAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'productc')
    list_display_links = ('id',)


admin.site.register(ProductAccess, ProductAccessAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link_to_video', 'duration')
    list_display_links = ('id', 'name', 'link_to_video')


admin.site.register(Lesson, LessonAdmin)


class LessonViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'viewing_time', 'status')
    list_display_links = ('id', 'user', 'status')


admin.site.register(LessonView, LessonViewAdmin)
# Register your models here.

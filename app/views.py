from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper


def get_lessons_by_user_and_product(request):
    if request.method == 'GET':
        user_id = request.GET.get('пользователь_id')
        # Найдем все продукты, к которым у пользователя есть доступ
        products = Product.objects.filter(productaccess__пользователь_id=user_id)
        # Получим все уроки, связанные с этими продуктами
        lessons = Lesson.objects.filter(продукты__in=products)
        # Посчитаем общее время просмотра уроков для пользователя
        total_time_watched = LessonView.objects.filter(
            пользователь_id=user_id, статус='Просмотрено').aggregate(
            total_time=Sum('время_просмотра'))['total_time']
        # Создадим список уроков с информацией о статусе и времени просмотра
        lessons_info = []
        for lesson in lessons:
            lesson_view = LessonView.objects.filter(
                пользователь_id=user_id, урок=lesson).first()
            if lesson_view:
                status = lesson_view.статус
                time_watched = lesson_view.время_просмотра
                last_viewed_date = lesson_view.дата_просмотра.strftime('%Y-%m-%d %H:%M:%S')
            else:
                status = 'Не просмотрено'
                time_watched = 0
                last_viewed_date = 'Нет данных'
            lessons_info.append({
                'название': lesson.название,
                'ссылка_на_видео': lesson.ссылка_на_видео,
                'длительность_урока': lesson.длительность,
                'статус': status,
                'время_просмотра': time_watched,
                'дата_последнего_просмотра': last_viewed_date
            })
        response_data = {
            'lessons': lessons_info,
            'общее_время_просмотра': total_time_watched if total_time_watched else 0
        }
        return JsonResponse(response_data)
    else:
        JsonResponse({'message': 'Not Get request'})


def get_lessons_by_user_and_product(request):
    if request.method == 'GET':
        user_id = request.GET.get('пользователь_id')
        product_id = request.GET.get('продукт_id')
        product = get_object_or_404(Product, id=product_id)
        if product.productaccess_set.filter(пользователь_id=user_id).exists():
            lessons = Lesson.objects.filter(продукты=product)
            lessons_info = []
            for lesson in lessons:
                lesson_view = LessonView.objects.filter(
                    пользователь_id=user_id, урок=lesson).first()
                if lesson_view:
                    status = lesson_view.статус
                    time_watched = lesson_view.время_просмотра
                    last_viewed_date = lesson_view.дата_просмотра.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    status = 'Не просмотрено'
                    time_watched = 0
                    last_viewed_date = 'Нет данных'
                lessons_info.append({
                    'название': lesson.название,
                    'ссылка_на_видео': lesson.ссылка_на_видео,
                    'длительность_урока': lesson.длительность,
                    'статус': status,
                    'время_просмотра': time_watched,
                    'дата_последнего_просмотра': last_viewed_date
                })
            return JsonResponse({'lessons': lessons_info})
        else:
            return JsonResponse({'message': 'У вас нет доступа к данному продукту'}, status=403)


def get_product_stats(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_stats = []
        for product in products:
            lesson_views = LessonView.objects.filter(
                урок__продукты=product, статус='Просмотрено')
            total_lessons_watched = lesson_views.count()
            total_time_watched = lesson_views.aggregate(
                total_time=Sum('время_просмотра'))['total_time']
            total_users = product.productaccess_set.count()
            if total_users > 0:
                acquisition_percentage = total_lessons_watched / total_users * 100
            else:
                acquisition_percentage = 0
            product_stats.append({
                'название_продукта': product.название,
                'количество_просмотренных_уроков': total_lessons_watched,
                'общее_время_просмотра': total_time_watched if total_time_watched else 0,
                'количество_учеников': total_users,
                'процент_приобретения': acquisition_percentage
            })
        return JsonResponse({'product_stats': product_stats})

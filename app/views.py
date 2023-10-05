from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.db.models import Count, Sum, Case, When, F, Value, IntegerField


from .models import *


@login_required
def lesson_list(request):
    user = request.user
    lesson_views = LessonView.objects.filter(user=user)
    return render(request, 'lesson_list.html', {'lesson_views': lesson_views})


@login_required
def product_lesson_list(request, product_id):
    user = request.user
    lessons = Lesson.objects.filter(products__productaccess__user=user, products__id=product_id)
    return render(request, 'product_lesson_list.html', {'lessons': lessons})


@login_required
def product_statistics(request):
    user = request.user
    products = Product.objects.annotate(
        total_lessons=Count('lessons'),
        total_students=Count('productaccess'),
        total_views=Sum(Case(
            When(lessons__lessonview__user=user, then=F('lessons__lessonview__viewing_time')),
            default=Value(0),
            output_field=IntegerField()
        )),
        purchase_percentage=Count('productaccess', filter=models.Q(productaccess__user=user)) / Count('productaccess')
    )
    return render(request, 'product_statistics.html', {'products': products})

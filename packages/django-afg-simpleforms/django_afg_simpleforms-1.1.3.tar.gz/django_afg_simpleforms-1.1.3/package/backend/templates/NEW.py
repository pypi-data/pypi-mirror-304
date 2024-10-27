# models.py
from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=200)  # Название блюда
    description = models.TextField()  # Описание блюда
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена блюда
    image = models.ImageField(upload_to='dishes/')  # Изображение блюда
    category = models.CharField(max_length=100, choices=[
        ('appetizer', 'Закуски'),
        ('main_course', 'Основные блюда'),
        ('dessert', 'Десерты'),
        ('beverage', 'Напитки')
    ])  # Категория блюда

    def _str_(self):
        return self.name


class Reservation(models.Model):
    name = models.CharField(max_length=100)  # Имя клиента
    phone = models.CharField(max_length=15)  # Телефон клиента
    date = models.DateField()  # Дата бронирования
    time = models.TimeField()  # Время бронирования
    guests_count = models.PositiveIntegerField()  # Количество гостей
    comment = models.TextField(blank=True)  # Комментарий (необязательное поле)

    def _str_(self):
        return f"{self.name} - {self.date} at {self.time}"


class Event(models.Model):
    title = models.CharField(max_length=200)  # Название мероприятия
    description = models.TextField()  # Описание мероприятия
    date = models.DateTimeField()  # Дата и время мероприятия
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Стоимость участия
    participants_count = models.PositiveIntegerField(default=0)  # Количество участников

    def _str_(self):
        return self.title



from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Reservation, Event
from .forms import ReservationForm  # Убедитесь, что у вас есть форма для бронирования


def dish_list(request):
    """
    Отображает список всех блюд.
    """
    dishes = Dish.objects.all()
    return render(request, 'dishes/dish_list.html', {'dishes': dishes})


def dish_detail(request, pk):
    """
    Отображает детали конкретного блюда.
    """
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, 'dishes/dish_detail.html', {'dish': dish})


def reservation_create(request):
    """
    Создание новой брони.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_success')  # перенаправление на страницу успеха
    else:
        form = ReservationForm()

    return render(request, 'reservations/reservation_form.html', {'form': form})


def event_list(request):
    """
    Отображает список всех мероприятий.
    """
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    """
    Отображает детали конкретного мероприятия.
    """
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})



from django.urls import path
from . import views

urlpatterns = [
    path('', views.dish_list, name='dish_list'),  # Главная страница со списком блюд
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),  # Страница с деталями блюда
    path('reservations/new/', views.reservation_create, name='reservation_create'),  # Создание новой брони
    path('events/', views.event_list, name='event_list'),  # Список мероприятий
    path('events/<int:pk>/', views.event_detail, name='event_detail'),  # Страница с деталями мероприятия
]
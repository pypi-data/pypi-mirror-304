from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .functions.email_sender import send_email
from .models import Media, Category, News, Order, Customer, IpModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import CreateUserForm, CreateProfileForm, LoginForm



def index(request):
    return render(request, 'base/index.html')


def illustration(request):
    categories = Category.objects.filter(name="Illustrations")

    paginated_categories = []
    for category in categories:
        media_list = category.media_set.all()
        paginator = Paginator(media_list, 9)

        page_number = request.GET.get('page', 1)
        try:
            media_page = paginator.page(page_number)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)

        paginated_categories.append({
            'category': category,
            'media_page': media_page,
        })

    context = {
        'paginated_categories': paginated_categories,
    }
    return render(request, 'base/base.html', context)


def engraving(request):
    categories = Category.objects.filter(name="Engravings")

    paginated_categories = []
    for category in categories:
        media_list = category.media_set.all()
        paginator = Paginator(media_list, 9)

        page_number = request.GET.get('page', 1)
        try:
            media_page = paginator.page(page_number)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)

        paginated_categories.append({
            'category': category,
            'media_page': media_page,
        })

    context = {
        'paginated_categories': paginated_categories,
    }
    return render(request, 'base/base.html', context)


def replica(request):
    categories = Category.objects.filter(name="Replicas")
    paginated_categories = []
    for category in categories:
        media_list = category.media_set.all()
        paginator = Paginator(media_list, 9)

        page_number = request.GET.get('page', 1)
        try:
            media_page = paginator.page(page_number)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)

        paginated_categories.append({
            'category': category,
            'media_page': media_page,
        })

    context = {
        'paginated_categories': paginated_categories,
    }
    return render(request, 'base/base.html', context)


def abstraction(request):
    categories = Category.objects.filter(name="Abstractions")
    paginated_categories = []
    for category in categories:
        media_list = category.media_set.all()
        paginator = Paginator(media_list, 9)

        page_number = request.GET.get('page', 1)
        try:
            media_page = paginator.page(page_number)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)

        paginated_categories.append({
            'category': category,
            'media_page': media_page,
        })

    context = {
        'paginated_categories': paginated_categories,
    }
    return render(request, 'base/base.html', context)


def interpretation(request):
    categories = Category.objects.filter(name="Interpretations")
    paginated_categories = []
    for category in categories:
        media_list = category.media_set.all()
        paginator = Paginator(media_list, 9)

        page_number = request.GET.get('page', 1)
        try:
            media_page = paginator.page(page_number)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)

        paginated_categories.append({
            'category': category,
            'media_page': media_page,
        })

    context = {
        'paginated_categories': paginated_categories,
    }
    return render(request, 'base/base.html', context)


def decorative_art(request):
    categories = Category.objects.filter(name="Decorative art")
    paginated_categories = []
    for category in categories:
        media_list = category.media_set.all()
        paginator = Paginator(media_list, 9)

        page_number = request.GET.get('page', 1)
        try:
            media_page = paginator.page(page_number)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)

        paginated_categories.append({
            'category': category,
            'media_page': media_page,
        })

    context = {
        'paginated_categories': paginated_categories,
    }
    return render(request, 'base/base.html', context)


def about(request):
    return render(request, 'base/about.html')


def contacts(request):
    return render(request, 'base/contacts.html')


def order_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        category_id = request.POST['category']
        description = request.POST.get('description', '')

        # Находим или создаем клиента по email
        customer, created = Customer.objects.get_or_create(email=email)

        # Создаем заказ
        category = Category.objects.get(category_id=category_id)
        order = Order.objects.create(
            customer_id=customer.customer_id,
            name=name,
            category=category,
            description=description
        )

        customer.order_count += 1
        customer.save()

        send_email(customer.customer_id, order.order_id)

        return redirect('order_success', name=name, email=email)

    else:
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'base/order_form.html', context)


def order_success(request, name, email):
    context = {
        'name': name,
        'email': email,
    }
    return render(request, 'base/order_success.html', context)


def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'base/detailed_news.html', {'news_item': news_item})


def news(request):
    sort_option = request.GET.get('sort', '-date')  # Параметр сортировки по умолчанию - от новых к старым
    news_list = News.objects.order_by(sort_option)
    paginator = Paginator(news_list, 3)  # Пагинация: по 3 новости на странице
    page = request.GET.get('page')
    try:
        news_pages = paginator.page(page)
    except PageNotAnInteger:
        news_pages = paginator.page(1)
    except EmptyPage:
        news_pages = paginator.page(paginator.num_pages)
    return render(request, 'base/news.html', {'news': news_pages, 'request': request})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def update_views(request):
    if request.method == 'GET' and 'media_id' in request.GET:
        media_id = request.GET.get('media_id')
        try:
            media_id = int(media_id)  # Ensure media_id is an integer
        except ValueError:
            return JsonResponse({'error': 'Invalid media_id. Must be an integer.'}, status=400)

        media = get_object_or_404(Media, pk=media_id)
        ip_address = get_client_ip(request)

        # Check if IP address has already viewed this media
        if not media.views.filter(ip_address=ip_address).exists():
            # Add new view
            if IpModel.objects.filter(ip_address=ip_address).exists():
                ip_model = IpModel.objects.get(ip_address=ip_address)
            else:
                ip_model = IpModel.objects.create(ip_address=ip_address)
            media.views.add(ip_model)

        views_count = media.get_unique_views_count()

        # Return JSON response with updated view count
        return JsonResponse({'views': views_count})
    else:
        return JsonResponse({'error': 'Invalid request. media_id parameter missing.'}, status=400)


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')

    user_form = CreateUserForm()
    profile_form = CreateProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration.html', context)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            print(form.errors)
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)


@login_required
def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        try:
            if form.is_valid():
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                table_number = form.cleaned_data['table']

                # Вычисляем временной диапазон для проверки
                start_time = datetime.combine(date, time)
                end_time = start_time + timedelta(hours=1)

                if start_time.hour >= 23 or start_time.hour < 10:
                    raise forms.ValidationError("Бронирование запрещено с 23:00 до 10:00.")

                # Проверяем наличие конфликта бронирования
                existing_reservations = Reservation.objects.filter(
                    table_id=table_number,
                    date=date,
                    time__range=(start_time.time(), end_time.time())
                )

                if existing_reservations.exists():
                    form.add_error(None, "Этот столик уже забронирован на выбранное время.")
                else:
                    form.save()
                    return redirect('index')  # замените на ваш URL
        except forms.ValidationError as e:
            form.add_error(None, e)
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {'form': form})


@login_required
def reserve_food(request):
    if request.method == 'POST':
        form = FoodReservationForm(request.POST)
        try:
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.save()
                return redirect('index')  # Замените на вашу страницу успешной бронь
        except ValueError as e:
            form.add_error(None, e)
    else:
        form = FoodReservationForm()

    return render(request, 'reserve_food.html', {'form': form})


@login_required
def user_profile(request):
    reservations = FoodReservation.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'reservations': reservations})
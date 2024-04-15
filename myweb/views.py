# Создайте пару представлений в вашем первом приложении:
# — главная
# — о себе.

# Внутри каждого представления должна быть переменная html — многострочный текст с HTML-вёрсткой и данными о вашем первом Django-сайте и о вас.

# Сохраняйте в логи данные о посещении страниц.
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render,redirect
from .models import Client, Product, Order
from .forms import ClientForm, ProductForm, OrderForm
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseServerError
import logging
from django.views import View
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import os
logger = logging.getLogger(__name__)


def home(request):
    html_text = '''
        <h1>Добро пожаловать!</h1>
        <p>Вы посетили мой первый Django - сайт</p>
    '''
    logger.info(f'Перешли на главную страницу.')
    return HttpResponse(html_text)


def info_about_me(request):
    html_text = '''
        <h2>Чуть-чуть обо мне.</h2>
        <p>Зовут меня Максим. Являюсь студентом GB.</p>
        <p>Мало времени на учёбу, но я стараюсь.</p>
        '''
    logger.info(f'Перешли на страницу с информацией обо мне.')
    return HttpResponse(html_text)

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return render(request, 'success.html', {'client_name': client.name})
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})

# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = form.save()
#             return render(request, 'success.html')
#     else:
#         form = ProductForm()
#     return render(request, 'create_product.html', {'form': form})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.photo = request.FILES.get('photo')  # сохраняем картинку
            product.save()

            # Опционально: изменить путь, если необходимо
            new_path = 'product_photos/{}'.format(product.photo.name)
            try:
                os.rename(product.photo.path, os.path.join(settings.MEDIA_ROOT, new_path))
                product.photo.name = new_path
                product.save()
            except FileNotFoundError:
                # Если возникает ошибка при переименовании, удалите уже созданный продукт
                product.delete()
                return HttpResponseServerError("Ошибка при переименовании файла")

            # Перенаправляем пользователя на страницу product_detail с использованием pk вместо product_id
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'create_product.html', {'form': form})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем объект Order и сохраняем его в базе данных
            order = form.save(commit=False)
            order.save()

            # Добавляем связанные товары в заказ
            selected_products = form.cleaned_data['products']
            for product in selected_products:
                order.products.add(product)
                order.total_amount += product.price

            # Сохраняем изменения в объекте Order
            order.save()

            return render(request, 'success.html')
    else:
        form = OrderForm()
    
    return render(request, 'create_order.html', {'form': form})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


def purchased_products(request):
    # Определяем даты начала и конца периода
    week_ago = timezone.now() - timedelta(days=7)
    month_ago = timezone.now() - timedelta(days=30)
    year_ago = timezone.now() - timedelta(days=365)

    # Получаем заказы клиента в указанных периодах времени и загружаем связанные с ними продукты
    week_orders = Order.objects.filter(order_date__gte=week_ago).prefetch_related('products')
    month_orders = Order.objects.filter(order_date__gte=month_ago).prefetch_related('products')
    year_orders = Order.objects.filter(order_date__gte=year_ago).prefetch_related('products')

    # Создаем словарь с информацией о товарах и заказах
    purchased_data = {
        'week_orders': week_orders,
        'month_orders': month_orders,
        'year_orders': year_orders,
    }

    # Получаем всех клиентов, связанных с этими заказами
    client_ids = list(week_orders.values_list('client_id', flat=True).distinct())
    clients = Client.objects.filter(id__in=client_ids)

    return render(request, 'purchased_products.html', {'purchased_data': purchased_data, 'clients': clients})

# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     return render(request, 'product_detail.html', {'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form})


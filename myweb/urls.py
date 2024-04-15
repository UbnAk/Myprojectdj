from django.urls import path,include # для определения шаблонов
from myweb import views
from .views import create_client,create_order,create_product,purchased_products,edit_product,product_detail


urlpatterns = [
    path('client/', views.create_client, name='client-view'),
    path('product/', views.create_product, name='create_product'),
    path('order/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('purchased_products/', views.purchased_products, name='purchased_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name = 'edit_product'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail')
]
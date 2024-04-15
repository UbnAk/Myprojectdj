from django.db import models

# Create your models here.

# Создайте три модели Django: клиент, товар и заказ. Клиент
# может иметь несколько заказов. Заказ может содержать
# несколько товаров. Товар может входить в несколько
# заказов.
# Поля модели "Клиент":
# ○ имя клиента
# ○ электронная почта клиента
# ○ номер телефона клиента
# ○ адрес клиента
# ○ дата регистрации клиента

class Client(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 20)
    address = models.TextField()
    registration_date = models.DateField()
    
    def __str__(self):
        return f'{self.name}' 

# Поля модели "Товар":
# ○ название товара
# ○ описание товара
# ○ цена товара
# ○ количество товара
# ○ дата добавления товара
    
# class Product(models.Model):
#     name_pr = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=8,decimal_places = 2)
#     quantity = models.PositiveIntegerField()
#     added_date = models.DateField()
    
    
#     def __str__(self):
#         return f'{self.name_pr}'
class Product(models.Model):
    name_pr = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    added_date = models.DateField()
    photo = models.ImageField(upload_to='product_photos/', blank=True)  # добавленное поле для фотографии
    
    def __str__(self):
        return self.name_pr
    
# Поля модели "Заказ":
# ○ связь с моделью "Клиент", указывает на клиента,
# сделавшего заказ
# ○ связь с моделью "Товар", указывает на товары,
# входящие в заказ
# ○ общая сумма заказа
# ○ дата оформления заказа

class Order(models.Model):
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    order_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
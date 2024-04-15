from django.contrib import admin
from .models import Order,Product,Client
# Register your models here.


@admin.action(description="Сбросить количество в ноль")
def update_(modeladmin, request, queryset):
    queryset.update(quantity=0)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_pr','description','price', 'quantity'] # Поля, отображаемые в списке продуктов
    ordering = ['name_pr', '-quantity']
    list_per_page = 4
    search_fields = ['name_pr']
    actions = [update_]

    
    fieldsets = [
        (
        'Продукт',
        {
        'classes': ['wide'],
        'fields': ['name_pr'],
        },
        ),
        (
        'Подробности',
        {
        'classes': ['collapse'],
        'description': 'Описание',
        'fields': ['description'],
        },
        ),
        (
        'Цена',
        {
        'fields': ['price'],
        }
        ),
        (
        'Количество и дата',
        {
        'description': 'Количество и дата',
        'fields': ['quantity','added_date'],
        }
        ),
        
        ]
    




class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    ordering = ['name']

    fieldsets = [
        (
        'Имя',
        {
        'classes': ['wide'],
        'fields': ['name'],
        },
        ),
        (
        'Почта',
        {

        'fields': ['email'],
        },
        ),
        (
        'Контактный номер',
        {
        'fields': ['phone_number'],
        }
        ),
        (
        'Адрес',
        {
        'fields': ['address'],
        }
        ),
        
        ]
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'total_amount', 'order_date', 'display_products')  # Добавляем метод display_products
    ordering = ['-order_date']
    list_per_page = 4

    def display_products(self, obj):
        return ", ".join([product.name_pr for product in obj.products.all()])


admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Client,ClientAdmin)

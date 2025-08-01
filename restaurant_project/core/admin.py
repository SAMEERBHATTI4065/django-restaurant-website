# Register your models here.
from django.contrib import admin
from .models import MenuItem, Category, Order, OrderItem, OrderDetails

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderDetails)



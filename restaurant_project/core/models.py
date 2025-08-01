from django.db import models
from django.contrib.auth.models import User

# Category like Pizza, Drink etc.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Menu Item
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# Order
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

# Order Item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

# ✅ NEW Model for Order Details (no conflict!)
class OrderDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Details for Order #{self.order.id}"

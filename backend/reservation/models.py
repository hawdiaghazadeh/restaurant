from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LookUps:
    LOCATION_LOOKUP = (
        ('vip', 'VIP'),
        ('window', 'Window'),
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('public', 'Public'),
    )

    RESERVATION_STATUS = (
        ('pending', 'Pending'),
        ('reserved', 'Reserved'),
        ('cancelled', 'Cancelled'),
    )

    MENU_CATEGORIES = (
        ('fast_food', 'Fast food'),
        ('sea_food', 'Sea food'),
        ('chines_food', 'Chines food'),
        ('italian_food', 'Italian food'),
        ('iranian_food', 'Iranian food'),
        ('desserts', 'Desserts'),
        ('drink', 'Drink')
    )

    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

class Table(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=20, choices=LookUps.LOCATION_LOOKUP)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.capacity})"


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=LookUps.RESERVATION_STATUS)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} | {self.table} ({self.guests}) | {self.date} | {self.from_time} - {self.to_time}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.CharField(max_length=20, choices=LookUps.MENU_CATEGORIES)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_item/', default='alternative/menu_item.png')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True )
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=LookUps.ORDER_STATUS , default='pending')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} | created by {self.user.email}'

    def update_total_price(self):
        self.total_price = sum(item.price for item in self.order_items.all())
        self.save(update_fields=['total_price'])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f'{self.quantity} x {self.menu_item.name} | {self.order} | {self.price}'

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total_price()





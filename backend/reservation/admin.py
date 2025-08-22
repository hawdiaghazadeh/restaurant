from django.contrib import admin

from .models import Reservation, Table, MenuItem, Order, OrderItem

class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ('user', 'table', 'date', 'from_time', 'to_time', 'guests', 'status')
    list_filter = ('status', 'date', 'table__location')
    search_fields = ('user__email', 'table__name')
    ordering = ('-date',)

class TableAdmin(admin.ModelAdmin):
    model = Table
    list_display = ('name', 'capacity', 'location', 'is_active', 'created_date')
    list_filter = ('is_active', 'created_date', 'location')
    search_fields = ('name',)
    ordering = ('-created_date',)

class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem
    list_display = ('name', 'description', 'price', 'category', 'is_available', 'created_date')
    list_filter = ('is_available', 'created_date', 'category')
    search_fields = ('name', 'description', )
    ordering = ('-created_date',)

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('user', 'reservation', 'total_price', 'status', 'created_date')
    list_filter = ('status', 'created_date')
    search_fields = ('user__email', 'reservation__table__name')
    ordering = ('-created_date',)

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('order', 'menu_item', 'quantity', 'price')
    list_filter = ('menu_item__category',)
    search_fields = ('order__user__email', 'order__reservation__table__name', 'menu_item__name')
    ordering = ('-order',)


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

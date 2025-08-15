from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class Users(admin.ModelAdmin):
    list_display = ('id', 'username', 'created_date', 'active')
    search_fields = ('username', 'create_date')
    list_filter = ('active',)
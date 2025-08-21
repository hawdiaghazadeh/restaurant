from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from .forms import UserCreationForm

class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Important dates', {'fields': ('created_date', 'updated_date', 'last_login')}),
    )
    readonly_fields = ('created_date', 'updated_date', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'user__email')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
   list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
   search_fields = ('email', 'username', 'first_name', 'last_name')
   ordering = ('email',)

   fieldsets = (
       (None, {'fields': ('username', 'email', 'password')}),
       ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'zip_code')}),
       ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
       ('Important dates', {'fields': ('last_login', 'date_joined')}),
   )

   add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'address', 'zip_code'),
       }),
   )



admin.site.register(CustomUser, CustomUserAdmin)

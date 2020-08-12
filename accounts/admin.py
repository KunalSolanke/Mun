from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roles', {'fields': ('role',)}),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Country)
admin.site.register(Team)
admin.site.register(DeligateProfile)
admin.site.register(Profile)

from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(UserProfile,UserAdmin)
admin.site.register(Country)
admin.site.register(Team)
admin.site.register(DeligateProfile)
admin.site.register(Profile)

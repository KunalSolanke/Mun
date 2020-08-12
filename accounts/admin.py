from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *



admin.site.register(User,UserAdmin)
admin.site.register(Country)
admin.site.register(Team)
admin.site.register(DeligateProfile)
admin.site.register(Profile)

# Register your models here.

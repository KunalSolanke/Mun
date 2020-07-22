from django.urls import path,include
from . import views
app_name = 'accounts'
urlpatterns = [
   path('login/',view= views.login,name= 'login')
]

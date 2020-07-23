from django.urls import path,include
from .views import *
app_name = 'accounts'
urlpatterns = [
   path('login/',view=login,name= 'login'),
   path('entry/',view=Entry,name='entry'),
   path('update/',view=Update,name='update'),
   path('logout/',view=logout_user,name='logout'),
]


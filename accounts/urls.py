from django.urls import path,include
from accounts.views import *
app_name = 'accounts'


urlpatterns = [
   path('login/',view=user_login,name= 'login'),
   path('entry/',view=createUsers,name='entry'),
   path('logout/',view=logout_user,name='logout'),
]


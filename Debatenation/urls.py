from djnago.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include
app_name = 'core'
urlpatterns = [
    path('DebateNation/sekrit/', admin.site.urls),
    path('account/',include('accounts.urls')),
    path('chits/',include('chits.urls'))
]
urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

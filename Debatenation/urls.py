from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import RedirectView

app_name = 'core'
urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('accounts/',include('accounts.urls')),
    path('chits/',include('chits.urls')),
    path('',RedirectView.as_view(url='/accounts/login')),
    path("favicon.ico/",RedirectView.as_view(url='/static/images/favicon.ico'))
]
urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

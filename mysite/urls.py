from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')), 
    path('', include('airbnb.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

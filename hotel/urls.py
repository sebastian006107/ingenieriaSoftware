from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservas.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

# Al final del archivo, después de urlpatterns:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
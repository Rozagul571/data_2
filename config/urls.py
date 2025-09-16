
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("data/", include("data.urls")),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


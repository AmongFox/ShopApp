from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path('auth/', include('auth_app.urls', namespace='auth_app')),
    path('profiles/', include('profiles_app.urls', namespace='profiles_app')),

    path('shop/', include('shop_app.urls', namespace='shop_app')),

    path('shop/', include('shop_app_api.urls', namespace='shop_app_api'))
]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    )

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import api_root

# Создаём главный роутер
router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
]

# Добавляем маршруты от роутера
urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
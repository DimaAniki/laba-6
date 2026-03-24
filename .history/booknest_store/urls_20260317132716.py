from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),           # Главная страница
    path('products/', include('products.urls')),  # Каталог товаров
    path('cart/', include('cart.urls')),      # Корзина
]

# Добавляем обработку медиафайлов (для изображений товаров)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    accounts_api_root,
    RegisterView,
    MyTokenObtainPairView,
    UserProfileView,
)
from rest_framework_simplejwt.views import TokenRefreshView

# Создаём роутер
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = 'accounts'

urlpatterns = [
    # Корневая страница Accounts API
    path('', accounts_api_root, name='accounts-api-root'),
    
    # Регистрация
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT токены
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Профиль
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Подключаем роутер (автоматически создаёт users/)
    path('', include(router.urls)),
]
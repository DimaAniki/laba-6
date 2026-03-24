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

# Создаём роутер для accounts
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user-accounts')

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
    
    # Подключаем роутер
    path('', include(router.urls)),
]
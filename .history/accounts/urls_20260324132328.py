from django.urls import path
from .views import (
    accounts_api_root,
    RegisterView,
    MyTokenObtainPairView,
    UserProfileView,
    PublicUserListView,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # Корневая страница Accounts API (должна быть ПЕРВОЙ!)
    path('', accounts_api_root, name='accounts-api-root'),
    
    # Регистрация нового пользователя
    path('register/', RegisterView.as_view(), name='register'),
    
    # Получение JWT токенов (login)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Обновление access токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Профиль текущего пользователя (требуется авторизация)
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Список всех пользователей (публичный доступ)
    path('users/', PublicUserListView.as_view(), name='user_list'),
]
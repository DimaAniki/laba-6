from django.urls import path
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    UserProfileView,
    PublicUserListView,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # Регистрация
    path('register/', RegisterView.as_view(), name='register'),
    
    # Вход (получение токенов)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Обновление токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Профиль пользователя
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Список пользователей (для демонстрации)
    path('users/', PublicUserListView.as_view(), name='user_list'),
]
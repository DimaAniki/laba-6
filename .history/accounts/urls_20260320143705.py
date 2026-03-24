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
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', PublicUserListView.as_view(), name='user_list'),
]
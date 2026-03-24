from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny  # ← Важно!
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLoginSerializer

User = get_user_model()


# ============================================================================
# API ROOT - Главная страница Accounts API
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def accounts_api_root(request, format=None):
    """Корневая страница Accounts API"""
    return Response({
        'message': 'BookNest Accounts API',
        'description': 'API для регистрации, авторизации и управления пользователями',
        'endpoints': {
            'register': {
                'url': '/api/accounts/register/',
                'method': 'POST',
                'description': 'Регистрация нового пользователя',
            },
            'login': {
                'url': '/api/accounts/login/',
                'method': 'POST',
                'description': 'Получение JWT токенов',
            },
            'token_refresh': {
                'url': '/api/accounts/token/refresh/',
                'method': 'POST',
                'description': 'Обновление access токена',
            },
            'profile': {
                'url': '/api/accounts/profile/',
                'method': 'GET, PUT, PATCH',
                'description': 'Профиль пользователя (требуется токен)',
            },
            'users_list': {
                'url': '/api/accounts/users/',
                'method': 'GET',
                'description': 'Список всех пользователей',
            }
        },
        'authentication': {
            'type': 'JWT Token',
            'header': 'Authorization: Bearer <token>'
        }
    })


# ============================================================================
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# ============================================================================

class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # ← Можно использовать AllowAny напрямую
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'success': True,
            'message': 'Пользователь успешно зарегистрирован',
            'user': {
                'id': serializer.data['id'],
                'email': serializer.data['email'],
                'full_name': serializer.data['full_name'],
            }
        }, status=status.HTTP_201_CREATED)


# ============================================================================
# JWT ТОКЕНЫ (LOGIN)
# ============================================================================

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор для получения JWT токенов"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
        }
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """Получение JWT токенов (access и refresh)"""
    serializer_class = MyTokenObtainPairSerializer


# ============================================================================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# ============================================================================

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля текущего пользователя"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # ← permissions.IsAuthenticated
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'user': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': 'Профиль успешно обновлён',
            'user': serializer.data
        })


# ============================================================================
# СПИСОК ПОЛЬЗОВАТЕЛЕЙ (для демонстрации)
# ============================================================================

class PublicUserListView(generics.ListAPIView):
    """Список всех пользователей (публичный доступ)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # ← AllowAny
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'success': True,
            'count': queryset.count(),
            'users': serializer.data
        })
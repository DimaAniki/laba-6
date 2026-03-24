from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLoginSerializer

User = get_user_model()


# ============================================================================
# API ROOT - Главная страница Accounts API
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def accounts_api_root(request, format=None):
    """
    Корневая страница Accounts API
    Список всех доступных endpoints для работы с пользователями
    """
    return Response({
        'message': 'BookNest Accounts API',
        'description': 'API для регистрации, авторизации и управления пользователями',
        'endpoints': {
            'register': {
                'url': '/api/accounts/register/',
                'method': 'POST',
                'description': 'Регистрация нового пользователя',
                'fields': {
                    'email': 'Email адрес (обязательно, уникальный)',
                    'full_name': 'Полное имя (обязательно)',
                    'phone': 'Номер телефона (необязательно)',
                    'password': 'Пароль (минимум 8 символов, обязательно)',
                    'password_confirm': 'Подтверждение пароля (обязательно)'
                }
            },
            'login': {
                'url': '/api/accounts/login/',
                'method': 'POST',
                'description': 'Получение JWT токенов (access и refresh)',
                'fields': {
                    'email': 'Email адрес',
                    'password': 'Пароль'
                }
            },
            'token_refresh': {
                'url': '/api/accounts/token/refresh/',
                'method': 'POST',
                'description': 'Обновление access токена',
                'fields': {
                    'refresh': 'Refresh токен'
                }
            },
            'profile': {
                'url': '/api/accounts/profile/',
                'method': 'GET, PUT, PATCH',
                'description': 'Просмотр и редактирование профиля текущего пользователя',
                'authentication': 'Требуется JWT токен (Authorization: Bearer <token>)'
            },
            'users_list': {
                'url': '/api/accounts/users/',
                'method': 'GET',
                'description': 'Список всех пользователей (публичный доступ)'
            }
        },
        'authentication': {
            'type': 'JWT (JSON Web Tokens)',
            'header': 'Authorization: Bearer <access_token>',
            'note': 'Для защищённых endpoints необходимо передать токен в заголовке'
        }
    })


# ============================================================================
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# ============================================================================

class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя
    
    POST /api/accounts/register/
    {
        "email": "user@example.com",
        "full_name": "Иван Иванов",
        "phone": "+79999999999",
        "password": "password123",
        "password_confirm": "password123"
    }
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
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
    """
    Кастомный сериализатор для получения JWT токенов
    Добавляет информацию о пользователе в ответ
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Добавляем кастомные claims в токен
        token['email'] = user.email
        token['full_name'] = user.full_name
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Добавляем информацию о пользователе в ответ
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
        }
        
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Получение JWT токенов (access и refresh)
    
    POST /api/accounts/login/
    {
        "email": "user@example.com",
        "password": "password123"
    }
    
    Response:
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhb...",
        "access": "eyJ0eXAiOiJKV1QiLCJhb...",
        "user": {
            "id": 1,
            "email": "user@example.com",
            "full_name": "Иван Иванов"
        }
    }
    """
    serializer_class = MyTokenObtainPairSerializer


# ============================================================================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# ============================================================================

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование профиля текущего пользователя
    
    GET /api/accounts/profile/ (требуется токен)
    PUT/PATCH /api/accounts/profile/ (требуется токен)
    
    Headers:
    Authorization: Bearer <access_token>
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Возвращает текущего авторизованного пользователя"""
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """Получение данных профиля"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'user': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Обновление данных профиля"""
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
    """
    Список всех пользователей (публичный доступ)
    
    GET /api/accounts/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'success': True,
            'count': queryset.count(),
            'users': serializer.data
        })
from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


# ============================================================================
# VIEWSET ДЛЯ ПОЛЬЗОВАТЕЛЕЙ (для Router)
# ============================================================================

class UserViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с пользователями (для отображения в API Root)
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Список всех пользователей"""
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            'success': True,
            'count': queryset.count(),
            'results': serializer.data
        })
    
    def retrieve(self, request, pk=None):
        """Получение конкретного пользователя"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'user': serializer.data
            })
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Пользователь не найден'
            }, status=status.HTTP_404_NOT_FOUND)


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
            'register': '/api/accounts/register/',
            'login': '/api/accounts/login/',
            'token_refresh': '/api/accounts/token/refresh/',
            'profile': '/api/accounts/profile/',
        }
    })


# ============================================================================
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# ============================================================================

class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
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
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
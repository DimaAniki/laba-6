from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    Корневая страница всего API проекта
    """
    return Response({
        'message': 'BookNest API v1.0',
        'description': 'API для интернет-магазина книг',
        'available_apis': {
            'accounts': reverse('accounts:accounts-api-root', request=request, format=format),
        },
        'endpoints': {
            'accounts_register': reverse('accounts:register', request=request, format=format),
            'accounts_login': reverse('accounts:token_obtain_pair', request=request, format=format),
            'accounts_profile': reverse('accounts:profile', request=request, format=format),
            'accounts_users': reverse('accounts:user-accounts-list', request=request, format=format),
        }
    })
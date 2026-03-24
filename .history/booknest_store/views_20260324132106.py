from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
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
            'accounts_register': '/api/accounts/register/',
            'accounts_login': '/api/accounts/login/',
            'accounts_profile': '/api/accounts/profile/',
            'accounts_users': '/api/accounts/users/',
        }
    })
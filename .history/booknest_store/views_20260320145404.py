from django.http import JsonResponse
from django.urls import reverse

def api_root(request):
    """Корневая страница API со списком всех endpoints"""
    return JsonResponse({
        'message': 'BookNest API v1.0',
        'description': 'API для интернет-магазина книг',
        'endpoints': {
            'register': '/api/accounts/register/',
            'login': '/api/accounts/login/',
            'token_refresh': '/api/accounts/token/refresh/',
            'profile': '/api/accounts/profile/',
            'users_list': '/api/accounts/users/',
        },
        'documentation': {
            'register_method': 'POST',
            'login_method': 'POST',
            'profile_method': 'GET/PUT (требуется токен)',
        }
    })
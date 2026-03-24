from django.http import JsonResponse

def api_root(request):
    """
    Корневая страница API со списком всех endpoints
    """
    return JsonResponse({
        'message': 'BookNest API v1.0',
        'description': 'API для интернет-магазина книг',
        'available_apis': {
            'accounts': '/api/accounts/',
        },
        'endpoints': {
            'accounts_register': '/api/accounts/register/',
            'accounts_login': '/api/accounts/login/',
            'accounts_token_refresh': '/api/accounts/token/refresh/',
            'accounts_profile': '/api/accounts/profile/',
            'accounts_users': '/api/accounts/users/',
        },
        'documentation': {
            'register_method': 'POST',
            'login_method': 'POST',
            'profile_method': 'GET/PUT (требуется токен)',
        }
    }, json_dumps_params={'ensure_ascii': False})
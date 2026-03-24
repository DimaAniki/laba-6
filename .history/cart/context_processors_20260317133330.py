# cart/context_processors.py

def cart_processor(request):
    """
    Добавляет объект корзины в контекст всех шаблонов.
    Теперь в любом HTML файле доступна переменная {{ cart }}
    """
    from cart.models import Cart  # Импорт внутри функции для безопасности
    
    cart = None
    
    # Пытаемся получить корзину по сессии (для всех пользователей)
    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
        except Cart.DoesNotExist:
            pass
            
    # Если пользователь вошёл в аккаунт, ищем его личную корзину
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            pass
            
    return {'cart': cart}
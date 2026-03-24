from .models import Cart

def cart_processor(request):
    """Добавляет корзину в контекст всех шаблонов"""
    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            return {'cart': cart}
        except Cart.DoesNotExist:
            pass
    return {'cart': None}
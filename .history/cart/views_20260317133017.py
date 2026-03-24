from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem
import json

def get_or_create_cart(request):
    """Получение или создание корзины"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Для анонимных пользователей используем сессию
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_view(request):
    """Отображение корзины"""
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

@require_POST
def add_to_cart(request):
    """Добавление товара в корзину (AJAX)"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)
    
    # Проверяем, есть ли уже такой товар в корзине
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'cart_total': cart.total_items,
        'message': f'Товар "{product.name}" добавлен в корзину'
    })

def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:cart')

def clear_cart(request):
    """Очистка корзины"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return redirect('cart:cart')

def checkout_view(request):
    """Оформление заказа"""
    cart = get_or_create_cart(request)
    
    if request.method == 'POST':
        # Здесь будет логика создания заказа
        # Пока просто очищаем корзину
        cart.items.all().delete()
        return render(request, 'cart/checkout_success.html')
    
    return render(request, 'cart/checkout.html', {'cart': cart})
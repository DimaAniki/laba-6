from django.shortcuts import render
from products.models import Product, Category

def home_view(request):
    """Главная страница"""
    
    popular_products = Product.objects.filter(available=True)[:6]
    categories = Category.objects.all()  # Получаем ВСЕ категории
    
    context = {
        'popular_products': popular_products,
        'categories': categories,  # Передаём в шаблон
    }
    return render(request, 'main/home.html', context)
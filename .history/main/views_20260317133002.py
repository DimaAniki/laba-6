from django.shortcuts import render
from products.models import Product, Category

def home_view(request):
    """Главная страница"""
    # Получаем популярные товары (последние добавленные)
    popular_products = Product.objects.filter(available=True)[:6]
    categories = Category.objects.all()
    
    context = {
        'popular_products': popular_products,
        'categories': categories,
    }
    return render(request, 'main/home.html', context)
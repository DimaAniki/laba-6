from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Создание тестовых данных для книг'

    def handle(self, *args, **kwargs):
        # Создаём категории
        categories = [
            {'name': 'Классика', 'slug': 'classic', 'description': 'Классическая литература'},
            {'name': 'Фэнтези', 'slug': 'fantasy', 'description': 'Миры магии и приключений'},
            {'name': 'Антиутопия', 'slug': 'dystopia', 'description': 'Мрачное будущее'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(**cat_data)
            self.stdout.write(f"✓ Категория: {cat_data['name']}")
        
        # Создаём книги
        books = [
            {
                'category': Category.objects.get(slug='classic'),
                'name': 'Война и мир',
                'slug': 'war-and-peace',
                'description': 'Эпопея Льва Толстого о жизни русского общества.',
                'price': 899.99,
                'stock': 25,
            },
            {
                'category': Category.objects.get(slug='dystopia'),
                'name': '1984',
                'slug': '1984',
                'description': 'Роман-антиутопия Джорджа Оруэлла.',
                'price': 599.99,
                'stock': 30,
            },
            {
                'category': Category.objects.get(slug='fantasy'),
                'name': 'Гарри Поттер',
                'slug': 'harry-potter',
                'description': 'Приключения юного волшебника.',
                'price': 799.99,
                'stock': 40,
            },
            {
                'category': Category.objects.get(slug='classic'),
                'name': 'Мастер и Маргарита',
                'slug': 'master-margarita',
                'description': 'Мистический роман Михаила Булгакова.',
                'price': 699.99,
                'stock': 20,
            },
            {
                'category': Category.objects.get(slug='fantasy'),
                'name': 'WoW: Артас',
                'slug': 'wow-artas',
                'description': 'История падения Артаса Менетила.',
                'price': 849.99,
                'stock': 15,
            },
            {
                'category': Category.objects.get(slug='dystopia'),
                'name': 'МЫ',
                'slug': 'we-zamyatin',
                'description': 'Антиутопия Евгения Замятина.',
                'price': 549.99,
                'stock': 18,
            },
        ]
        
        for book_data in books:
            Product.objects.get_or_create(
                slug=book_data['slug'],
                defaults=book_data
            )
            self.stdout.write(f"✓ Книга: {book_data['name']}")
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Тестовые данные успешно созданы!'))
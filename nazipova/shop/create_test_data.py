import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from shopik.models import Category, Product

categories = [
    'Электроника',
    'Одежда',
    'Книги',
    'Игрушки',
    'Красота',
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)

products_data = [
    {
        'name': 'Смартфон',
        'price': 29999.99,
        'stock': 10,
        'category': 'Электроника',
        'description': 'Мощный смартфон с отличной камерой'
    },
    {
        'name': 'Футболка',
        'price': 1999.99,
        'stock': 50,
        'category': 'Одежда',
        'description': 'Хлопковая футболка с принтом'
    },
    {
        'name': 'Роман',
        'price': 599.99,
        'stock': 25,
        'category': 'Книги',
        'description': 'Захватывающий роман от известного автора'
    },
    {
        'name': 'Конструктор',
        'price': 2999.99,
        'stock': 15,
        'category': 'Игрушки',
        'description': 'Развивающий конструктор для детей'
    },
    {
        'name': 'Помада',
        'price': 899.99,
        'stock': 30,
        'category': 'Красота',
        'description': 'Стойкая матовая помада'
    },
]

for product_data in products_data:
    category = Category.objects.get(name=product_data['category'])
    Product.objects.get_or_create(
        category=category,
        name=product_data['name'],
        price=product_data['price'],
        stock=product_data['stock'],
        description=product_data['description']
    )

print("Тестовые данные созданы!")
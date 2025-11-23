import os
import django
from django.db.models import Sum
from django.db.models.expressions import result

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Order
from django.db.models import Q, F
#
#
# def product_quantity_ordered():
#     orders = (Product.objects
#               .annotate(total = Sum('orderproduct__quantity'))
#               .exclude(total=None)
#               .values('name', 'total')
#               .order_by('-total')
#               )
#     return '\n'.join(f"Quantity ordered of {order['name']}: {order['total']}" for order in orders)
#
# # print(product_quantity_ordered())


# def ordered_products_per_customer():
#     orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')
#
#     result = []
#     for o in orders:
#         result.append(f"Order ID: {o.id}, Customer: {o.customer.username}")
#         for ordered_product in o.orderproduct_set.all():
#             result.append(f"- Product: {ordered_product.product.name}, "
#                           f"Category: {ordered_product.product.category.name}")
#     return '\n'.join(result)


# print(ordered_products_per_customer())
#
# def filter_products():
#     query = Q(is_available=True) & Q(price__gte=3.00)
#     products = Product.objects.filter(query).order_by('-price', 'name')
#     return '\n'.join(f"{p.name}: {p.price}lv." for p in products)
#
# print(filter_products())

def give_discount():
    query = Q(price__gt=3) & Q(is_available=True)
    to_discount_products = Product.objects.filter(query)
    to_discount_products.update(price=F('price') * 0.7)
    available_products = Product.objects.filter(is_available=True).order_by('-price', 'name')
    return '\n'.join(f"{p.name}: {p.price}lv." for p in available_products)

# print(give_discount())



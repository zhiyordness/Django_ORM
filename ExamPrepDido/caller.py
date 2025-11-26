import os
from email.policy import default
from typing import Optional

import django
from django.db.models import Q, F, Case, When, Value
from django.db.models.aggregates import Count
from pprint import pp
from django.db import connection

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.helpers import populate_model_with_data
from main_app.models import Profile, Product, Order

# Create queries within functions


def populate_db() -> None:
    populate_model_with_data(Profile)
    populate_model_with_data(Product)
    populate_model_with_data(Order)



def get_profiles(search_string: Optional[str]=None) -> str:

    if not search_string:
        return ""

    profiles = Profile.objects.annotate(
        orders_count=Count('order')
    ).filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if profiles:
        result = []
        for p in profiles:
            result.append(f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders_count}")
        return '\n'.join(result)

    return ""


def get_loyal_profiles() -> str:

    return '\n'.join(
        f"Profile: {p.full_name}, orders: {p.count_orders}"
        for p in Profile.objects.get_regular_customers()
    )


def get_last_sold_products() -> str:

    last_order = Order.objects.last()

    if not last_order:
        return ""

    return f"Last sold products: {', '.join(p.name for p in last_order.products.all().order_by('order__products__name'))}"


def get_top_products() -> str:

    top_products = Product.objects.annotate(
        orders_count=Count('order')
    ).order_by('-orders_count',
             'name')[:5]
    if not top_products.exists():
        return ""

    return f"Top products:\n" + '\n'.join(f"{p.name}, sold {p.orders_count} times" for p in top_products)


def apply_discounts() -> str:

    orders = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        is_completed=False,
        products_count__gt=2
    ).update(
        total_price = F('total_price') * 0.90
    )
    return f"Discount applied to {orders} orders."



def complete_order() -> str:
    first_order = Order.objects.filter(
        is_completed=False
    ).order_by('creation_date').first()

    if not first_order:
        return ""

    first_order.is_completed = True

    Product.objects.filter(
        order=first_order
    ).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )
    first_order.save()

    return f"Order has been completed!"


# print(complete_order())
# pp(connection.queries)
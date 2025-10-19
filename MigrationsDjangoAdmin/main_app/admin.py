from django.contrib import admin
from decimal import Decimal
from main_app.models import Product

#admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'price', 'created_on')
    search_fields = ('name', 'category', 'supplier')
    list_filter = ('supplier', 'category')


    fieldsets = (
        ('General Information', {'fields': ('name', 'description', 'price', 'barcode', )}),
        ('Categorization', {'fields': ('category', 'supplier')}),
    )

    date_hierarchy = 'created_on'

from django.contrib import admin
from .models import (Product, Category, Supplier, Buyer, Order,
                     Delivery, OrderItem, DeliveryItem)


admin.site.register(OrderItem)


@admin.register(DeliveryItem)
class DeliveryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'product', 'quantity')
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'quantity', 'price', 'get_total_price')
    list_filter = ('category__name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'created_at', 'status', 'items_set', 'total_values')
    inlines = (DeliveryItemInline,)

    def items_set(self, obj):
        return ', '.join(f'{i.product.name} - {i.quantity}' for i in obj.items.all())

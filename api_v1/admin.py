from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (User, Product, Category, Supplier, Buyer, Order,
                     Delivery, OrderItem, DeliveryItem)


admin.site.register(OrderItem)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'email', 'role')
    list_filter = ('role',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


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
    list_display = ('id', 'name', 'category', 'quantity', 'price', 'total_price')
    list_filter = ('category__name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'created_at', 'status',)
    inlines = (OrderItemInline,)


class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'created_at', 'status', 'items_set', 'total_values')
    inlines = (DeliveryItemInline,)

    def items_set(self, obj):
        return ', '.join(f'{i.product.name} - {i.quantity}' for i in obj.items.all())

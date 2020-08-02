from rest_framework import serializers
from .models import Delivery, Product, Category, Supplier, DeliveryItem


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров"""
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('__all__')


class SupplierSerializer(serializers.ModelSerializer):
    """Сериализатор для поставщиков"""
    product_category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ('__all__')


class DeliveryItemSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для количества товаров в поставке"""
    class Meta:
        model = DeliveryItem
        fields = ('product', 'quantity')


class DeliverySerializer(serializers.ModelSerializer):
    """Сериализатор поставки товаров"""
    items = DeliveryItemSerializer(many=True)

    class Meta:
        model = Delivery
        fields = ('supplier', 'items')

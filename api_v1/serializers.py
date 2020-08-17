from rest_framework import serializers
from django.contrib.auth import password_validation, get_user_model
from rest_framework.generics import get_object_or_404
from .models import (Delivery, Product, Category, Supplier, DeliveryItem,
                     OrderItem, Order, Buyer)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_email(self, value):
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'User with this email address exists'
            )
        return value

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.create_user(**validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')


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


class BuyerSerializer(serializers.ModelSerializer):
    """Сериализатор для покупателя"""
    class Meta:
        model = Buyer
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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        delivery = Delivery.objects.create(**validated_data)
        for item_data in items_data:
            DeliveryItem.objects.create(delivery=delivery, **item_data)
            product = item_data['product']
            product.quantity += item_data['quantity']
            product.save()
        return delivery


class OrderItemSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для количества товаров в заказе"""
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                f'Quantity of items must be must be greater than zero'
            )
        return value

    def validate(self, data):
        product = data['product']
        if product.quantity < data['quantity']:
            raise serializers.ValidationError(
                f'Not enough items of {product}, '
                f'available only {product.quantity} items, '
                f'requested {data["quantity"]} items'
            )
        return data


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказа"""
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('buyer', 'items')

    def create(self, validated_data):
        items_validated_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_validated_data:
            OrderItem.objects.create(order=order, **item_data)
            product = item_data['product']
            product.quantity -= item_data['quantity']
            product.save()
        return order


class BuyerDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о покупателе"""
    orders = OrderSerializer(many=True)

    class Meta:
        model = Buyer
        fields = ('__all__')

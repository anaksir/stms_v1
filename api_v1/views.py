from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import (get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .models import Product, Category, Supplier, Delivery, User, Order, Buyer
from .serializers import (ProductSerializer, CategorySerializer,
                          CategoryCreateSerializer,
                          SupplierSerializer, DeliverySerializer,
                          UserSerializer, OrderSerializer, BuyerSerializer,
                          BuyerDetailSerializer)
from django.db.models import Count, Sum, F


class MultipeSerializersViewSetMixin:
    action_serializers = None

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)


class SupplierView(APIView):
    def get(self, request):
        products = Supplier.objects.all()
        serializer = SupplierSerializer(products, many=True)
        return Response({'suppliers': serializer.data})


class BuyerViewSet(viewsets.ModelViewSet):
    """ViewSet для отображения покупателей"""
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

    action_serializers = {
        'retrieve': BuyerDetailSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)


class ProductViewSet(viewsets.ModelViewSet):
    """Тестовый ViewSet для отображения товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(MultipeSerializersViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для отображения категорий"""
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    action_serializers = {
        'create': CategoryCreateSerializer,
    }

    def get_queryset(self):
        """
        Возвращает queryset с аннотацией количеством товаров категории и
        суммой стоимости товаров в категории
        """
        return Category.objects.annotate(
            number_of_products=Count('products'),
            total_items=Sum('products__quantity'),
            total_value=Sum(F('products__quantity') * F('products__price'))
        )


class SingleCategoryView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    """Тестовый ViewSet для отображения поставки"""
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для отображения заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False)
    def recent_orders(self, request):
        """
        Показывает по умолчанию последние 10 заказов,
        или показывает число, указнное в GET-параметре limit.
        """
        orders_limit = self.request.query_params.get('limit', '10')
        try:
            orders_limit = int(orders_limit)
        except ValueError:
            orders_limit = 10
        recent_orders = (
            Order.objects.all().order_by('-created_at')[:orders_limit]
        )
        serializer = self.get_serializer(recent_orders, many=True)
        return Response(serializer.data)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

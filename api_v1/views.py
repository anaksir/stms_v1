from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import (get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import UserPermission
from .models import Product, Category, Supplier, Delivery, User, Order, Buyer
from .serializers import (ProductSerializer, CategorySerializer,
                          CategoryCreateSerializer,
                          SupplierSerializer, DeliverySerializer,
                          UserSerializer, OrderSerializer, BuyerSerializer,
                          BuyerDetailSerializer, SupplierDetailSerializer,
                          ProductCreateSerializer)
from django.db.models import Count, Sum, F


class MultipeSerializersViewSetMixin:
    """
    Mixin для ViewSet, для выбора отдельных Serializer'ов для разных действий
    """
    action_serializers = None

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)


class SupplierViewSet(MultipeSerializersViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для отображения поставщиков"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    action_serializers = {
        'retrieve': SupplierDetailSerializer,
    }


class BuyerViewSet(viewsets.ModelViewSet):
    """ViewSet для отображения покупателей"""
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

    action_serializers = {
        'retrieve': BuyerDetailSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)


class ProductViewSet(MultipeSerializersViewSetMixin, viewsets.ModelViewSet):
    """ ViewSet для отображения товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    action_serializers = {
        'create': ProductCreateSerializer,
    }


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


class DeliveryViewSet(viewsets.ModelViewSet):
    """Тестовый ViewSet для отображения поставки"""
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Выбираем поставки, относящиеся к окнкретному пользователю,
        или, если пользователь относится к персооналу, показать все
        """
        user = self.request.user
        if user.is_staff:
            queryset = Delivery.objects.all()
        else:
            queryset = Delivery.objects.filter(supplier=user.supplier_profile)
        return queryset


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


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (UserPermission,)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated and user.role == 'a':
    #         queryset = User.objects.all()
    #     else:
    #         queryset = user
    #     return queryset


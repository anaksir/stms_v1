from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .models import Product, Category, Supplier, Delivery, User, Order, Buyer
from .serializers import (ProductSerializer, CategorySerializer,
                          SupplierSerializer, DeliverySerializer,
                          UserSerializer, OrderSerializer, BuyerSerializer,
                          BuyerDetailSerializer)


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


class CategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

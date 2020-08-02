from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from .models import Product, Category, Supplier
from .serializers import (ProductSerializer, CategorySerializer,
                          SupplierSerializer)


class SupplierView(APIView):
    def get(self, request):
        products = Supplier.objects.all()
        serializer = SupplierSerializer(products, many=True)
        return Response({'suppliers': serializer.data})


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

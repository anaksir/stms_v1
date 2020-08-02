from django.urls import path
from .views import (ProductViewSet, CategoryView, SupplierView,
                    SingleCategoryView)
from .yasg import urlpatterns as swagger_urls
from rest_framework.routers import DefaultRouter


app_name = "api_v1"

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('categories/', CategoryView.as_view()),
    path('categories/<int:pk>', SingleCategoryView.as_view()),
    path('suppliers/', SupplierView.as_view()),
]

urlpatterns += swagger_urls
urlpatterns += router.urls

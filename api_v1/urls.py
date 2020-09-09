from django.urls import path, include
from .views import (ProductViewSet, CategoryViewSet, SupplierViewSet,
                    DeliveryViewSet, HelloView,
                    UserListView, OrderViewSet, BuyerViewSet)
from .yasg import urlpatterns as swagger_urls
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


app_name = "api_v1"

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('deliveries', DeliveryViewSet, basename='delivery')
router.register('orders', OrderViewSet, basename='order')
router.register('buyers', BuyerViewSet, basename='buyer')
router.register('categories', CategoryViewSet, basename='category')
router.register('suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('token/',
         jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('users/', UserListView.as_view(), name='users'),
]

urlpatterns += swagger_urls
urlpatterns += router.urls

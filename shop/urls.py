from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet, UserProfile
from django.urls import path


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'product-images', ProductImageViewSet, basename='product-images')

urlpatterns = router.urls + [
    path('profile/', UserProfile.as_view(), name='profile'),
]

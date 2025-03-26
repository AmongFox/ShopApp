from django.urls import path
from .views import CartProductCreateView, CartProductDeleteView, FavoriteProductCreateView, FavoriteProductDeleteView

app_name = 'shop_app_api'

urlpatterns = [
    path('product/api/cart/create/', CartProductCreateView.as_view(), name='cart_product_create'),
    path('product/api/cart/delete/<int:pk>/', CartProductDeleteView.as_view(), name='cart_product_delete'),

    path('product/api/favorite/create/', FavoriteProductCreateView.as_view(), name='favorite_product_create'),
    path('product/api/favorite/delete/<int:pk>/', FavoriteProductDeleteView.as_view(), name='favorite_product_delete'),
]

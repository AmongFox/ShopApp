from django.urls import path
from .views import AddToCartAPIView, RemoveFromCartAPIView, AddToFavoriteAPIView, FavoriteProductDeleteView, \
    OrderCreateView, SelectedProductsAPI

app_name = 'shop_app_api'

urlpatterns = [
    path('product/api/cart/add/', AddToCartAPIView.as_view(), name='product_add_to_cart'),
    path('product/api/cart/remove/<int:pk>/', RemoveFromCartAPIView.as_view(), name='product_remove_from_cart'),

    path('product/api/favorite/add/', AddToFavoriteAPIView.as_view(), name='product_add_to_favorite'),
    path('product/api/favorite/remove/<int:pk>/', FavoriteProductDeleteView.as_view(), name='product_remove_from_favorite'),

    path('orders/api/create/', OrderCreateView.as_view(), name='create_order'),

    path('checkout/api/selected-products/', SelectedProductsAPI.as_view(), name='selected_products')
]

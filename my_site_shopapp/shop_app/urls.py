from django.urls import path

from .views import (
    ShopMainPageView,
    ProductDetailView,
    ProductListView,
    MyProductView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CartProductListView,
    FavoriteProductListView,
    CheckoutView,
)

app_name = "shop_app"

urlpatterns = [
    path("", ShopMainPageView.as_view(), name="shop_main_page"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("list/", ProductListView.as_view(), name="product_list"),
    path("product/my/", MyProductView.as_view(), name="my_product"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("cart/", CartProductListView.as_view(), name="cart_product_list"),
    path("favorite/", FavoriteProductListView.as_view(), name="favorite_product_list"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]

from rest_framework import serializers
from .models import CartProduct, FavoriteProduct, Order, OrderItem
from shop_app.models import ProductModel


class CartProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductModel.objects.all(),
        source='product',
        write_only=True,
    )

    class Meta:
        model = CartProduct
        fields = ['pk', 'product', 'product_id', 'quantity']
        read_only_fields = ['product']
        extra_kwargs = {
            'quantity': {'min_value': 1}
        }


class FavoriteProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductModel.objects.all(),
        source='product',
        write_only=True,
    )

    class Meta:
        model = FavoriteProduct
        fields = ['pk', 'product', 'product_id']
        read_only_fields = ['product']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_price', 'items'
        ]
        read_only_fields = ['user, status, total_price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['pk', 'name', 'price', 'description']

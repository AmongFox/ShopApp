from rest_framework import serializers
from .models import CartProduct, FavoriteProduct


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['pk', 'user', 'product', 'quantity']


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ['pk', 'user', 'product']

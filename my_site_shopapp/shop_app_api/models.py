from shop_app.models import ProductModel
from auth_app.models import CustomUserModel
from django.db import models


class CartProduct(models.Model):
    """Cart Product"""
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='cart_product')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.product.pk} товар — {self.product.name!r}'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='favorite_product')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='favorite_product')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self) -> str:
        return f'{self.product.pk} товар — {self.product.name!r}'

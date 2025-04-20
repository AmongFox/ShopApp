from shop_app.models import ProductModel
from auth_app.models import CustomUserModel
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name='cart')


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self) -> str:
        return f'{self.product.pk} товар — {self.product.name!r}'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='favorite')


class FavoriteProduct(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='favorite_products')

    class Meta:
        unique_together = ('favorite', 'product')

    def __str__(self) -> str:
        return f'{self.product.pk} товар — {self.product.name!r}'


class Order(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('created', 'Создан'),
            ('paid', 'Оплачен'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
            ('canceled', 'Отменен'),
        ],
        default='Создан'
    )
    total_price = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} - {self.product.name}'

from django.db import models
from auth_app.models import CustomUserModel
from django_resized import ResizedImageField


def product_preview_directory_path(instance: "ProductModel", filename: str) -> str:
    return f"products/product_{instance.pk}/{filename}"


class ProductModel(models.Model):
    """Product"""
    name = models.CharField(max_length=60, db_index=True)
    description = models.TextField(max_length=500, null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUserModel, on_delete=models.PROTECT)
    archived = models.BooleanField(default=False)
    preview = ResizedImageField(null=False, upload_to=product_preview_directory_path)

    def __str__(self) -> str:
        return f'{self.pk} Продукт — {self.name!r}'

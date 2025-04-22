from django import forms
from django.utils.translation import gettext_lazy as _

from shop_app_api.models import Order

from .models import ProductModel


class ProductForm(forms.ModelForm):
    name = forms.CharField(label=_("Название"), max_length=60)
    description = forms.CharField(label=_("Описание"), max_length=1000)
    price = forms.DecimalField(
        label=_("Цена"), min_value=0, max_digits=8, decimal_places=2
    )
    discount = forms.IntegerField(
        label=_("Скидка"), min_value=0, max_value=100, step_size=5, required=False
    )
    quantity = forms.IntegerField(
        label=_("Количество"), min_value=0, max_value=1000, step_size=10, required=False
    )
    # archived = forms.BooleanField(label=_('Архив'))

    class Meta:
        model = ProductModel
        fields = [
            "name",
            "description",
            "price",
            "discount",
            "quantity",
            "archived",
            "preview",  # ResizedImageField field
        ]

    def save(self, user=None, commit=True):
        product = super().save(commit=False)

        if user:
            product.created_by = user
        if commit:
            product.save()

        product.preview = self.cleaned_data["preview"]

        if commit:
            product.save()

        return product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user",
            # 'created_at',
            "status",
            "total_price",
        ]


class CheckoutForm(forms.Form):
    name = forms.CharField(label="ФИО", max_length=100)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Телефон", max_length=20)
    address = forms.CharField(label="Адрес доставки", widget=forms.Textarea)
    comment = forms.CharField(
        label="Комментарий к заказу", widget=forms.Textarea, required=False
    )

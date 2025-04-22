from django import forms
import django_filters

from .models import ProductModel


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Поиск",
                "autocomplete": "off",
                "class": "search-input",
            }
        ),
        lookup_expr="icontains",
        field_name="name",
    )

    price = django_filters.RangeFilter(
        label="Цена",
        widget=django_filters.widgets.RangeWidget(
            attrs={
                "placeholder": "...",
            }
        ),
        field_name="price",
    )

    archived = django_filters.BooleanFilter(
        label="Архивированные",
        widget=forms.CheckboxInput(),
        field_name="archived",
    )
    in_stock = django_filters.BooleanFilter(
        label="В наличии",
        widget=forms.CheckboxInput(),
        field_name="in_stock",
        method="filter_in_stock",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["in_stock"].extra["initial"] = True

    class Meta:
        model = ProductModel
        fields = ["name", "price", "archived"]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(quantity__gt=0)

        else:
            return queryset

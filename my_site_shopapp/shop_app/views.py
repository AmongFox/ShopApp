import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from profiles_app.models import UserProfileModel
from shop_app_api.models import Cart, CartProduct, Favorite, FavoriteProduct
from shop_app_api.serializers import ProductSerializer

from .filters import ProductFilter
from .forms import CheckoutForm, OrderForm, ProductForm
from .models import ProductModel


class ShopMainPageView(ListView):
    """View для отображения главной страницы магазина с фильтрацией товаров.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для списка товаров.
        model (Model): Модель товара.

    Methods:
        get_queryset: Возвращает отфильтрованный QuerySet товаров.
        get_context_data: Добавляет в контекст форму фильтрации и данные пользователя.
    """

    template_name = "shop-main.html"
    context_object_name = "products"
    model = ProductModel

    def get_queryset(self):
        """Возвращает QuerySet товаров с применением фильтров.

        Returns:
            QuerySet: Отфильтрованный список товаров.
        """
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Добавляет в контекст форму фильтрации и данные пользователя.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context["my_user"] = user
            context["profile"] = get_object_or_404(UserProfileModel, user=user)

        context["form"] = self.filterset.form
        return context


class ProductDetailView(DetailView):
    """View для отображения детальной информации о товаре.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для товара.
        model (Model): Модель товара.

    Methods:
        get_context_data: Добавляет текущего пользователя в контекст.
    """

    template_name = "product-detail.html"
    context_object_name = "product"
    model = ProductModel

    def get_context_data(self, **kwargs):
        """Добавляет текущего пользователя в контекст шаблона.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["my_user"] = user
        return context


class ProductListView(ListView):
    """View для отображения списка всех товаров с фильтрацией.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для списка товаров.
        model (Model): Модель товара.

    Methods:
        get_queryset: Возвращает отфильтрованный QuerySet товаров.
        get_context_data: Добавляет в контекст форму фильтрации и данные пользователя.
    """

    template_name = "product-list.html"
    context_object_name = "products"
    model = ProductModel

    def get_queryset(self):
        """Возвращает QuerySet товаров с применением фильтров.

        Returns:
            QuerySet: Отфильтрованный список товаров.
        """
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Добавляет в контекст форму фильтрации и данные пользователя.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context["my_user"] = user
            context["profile"] = get_object_or_404(UserProfileModel, user=user)

        context["form"] = self.filterset.form
        return context


class MyProductView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """View для отображения списка товаров текущего пользователя (staff).

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для списка товаров.
        model (Model): Модель товара.
        form_class (Form): Класс формы для фильтрации.

    Methods:
        has_permission: Проверяет, является ли пользователь staff.
        handle_no_permission: Обрабатывает отказ в доступе.
        get_queryset: Возвращает товары, созданные текущим пользователем.
        get_context_data: Добавляет данные пользователя и форму поиска в контекст.
    """

    template_name = "my-product.html"
    context_object_name = "products"
    model = ProductModel
    form_class = ProductFilter

    def has_permission(self):
        """Проверяет права доступа.

        Returns:
            bool: True если пользователь является staff.
        """
        return self.request.user.is_staff

    def handle_no_permission(self):
        """Обрабатывает отказ в доступе.

        Returns:
            HttpResponse: Рендер страницы с ошибкой доступа.
        """
        return render(self.request, "error/product-forbidden.html")

    def get_queryset(self):
        """Возвращает товары, созданные текущим пользователем.

        Returns:
            QuerySet: Список товаров пользователя.
        """
        return ProductModel.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        """Добавляет данные пользователя и форму поиска в контекст.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        context["profile"] = get_object_or_404(UserProfileModel, user=self.request.user)
        context["search_form"] = self.form_class(self.request.GET)
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """View для создания нового товара.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для товара.
        form_class (Form): Класс формы для создания товара.
        model (Model): Модель товара.

    Methods:
        has_permission: Проверяет, является ли пользователь staff.
        handle_no_permission: Обрабатывает отказ в доступе.
        form_valid: Обрабатывает валидную форму и сохраняет товар.
        form_invalid: Обрабатывает невалидную форму.
    """

    template_name = "product-create.html"
    context_object_name = "product"
    form_class = ProductForm
    model = ProductModel

    def has_permission(self):
        """Проверяет права доступа.

        Returns:
            bool: True если пользователь является staff.
        """
        return self.request.user.is_staff

    def handle_no_permission(self):
        """Обрабатывает отказ в доступе.

        Returns:
            HttpResponse: Рендер страницы с ошибкой доступа.
        """
        return render(self.request, "error/product-forbidden.html")

    def form_valid(self, form):
        """Обрабатывает валидную форму и сохраняет товар.

        Args:
            form: Валидная форма товара.

        Returns:
            HttpResponseRedirect: Перенаправление на список товаров.
        """
        product = form.save(user=self.request.user, commit=True)
        product.save()
        return redirect(reverse("shop_app:product_list"))

    def form_invalid(self, form):
        """Обрабатывает невалидную форму.

        Args:
            form: Невалидная форма товара.

        Returns:
            HttpResponse: Рендер страницы с формой и ошибками.
        """
        print("Form is invalid:", form.errors)
        return render(
            self.request, self.template_name, {"form": form, "product": form.instance}
        )


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """View для обновления информации о товаре.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для товара.
        model (Model): Модель товара.
        form_class (Form): Класс формы для редактирования товара.

    Methods:
        has_permission: Проверяет, является ли пользователь staff и создателем товара.
        handle_no_permission: Обрабатывает отказ в доступе.
        form_valid: Обрабатывает валидную форму и сохраняет изменения.
    """

    template_name = "product-update.html"
    context_object_name = "product"
    model = ProductModel
    form_class = ProductForm

    def has_permission(self):
        """Проверяет права доступа.

        Returns:
            bool: True если пользователь является staff и создателем товара.
        """
        self.object = self.get_object()
        return (
            self.request.user.is_staff and self.request.user == self.object.created_by
        )

    def handle_no_permission(self):
        """Обрабатывает отказ в доступе.

        Returns:
            HttpResponse: Рендер страницы с ошибкой доступа.
        """
        return render(self.request, "error/product-forbidden.html")

    def form_valid(self, form):
        """Обрабатывает валидную форму и сохраняет изменения.

        Args:
            form: Валидная форма товара.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу товара.
        """
        product = form.save(commit=False)
        product.save()
        return redirect(
            reverse("shop_app:product_detail", kwargs={"pk": self.object.pk})
        )


class ProductDeleteView(DeleteView):
    """View для удаления товара.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для товара.
        model (Model): Модель товара.
    """

    template_name = "product-delete.html"
    context_object_name = "product"
    model = ProductModel


class CartProductListView(LoginRequiredMixin, ListView):
    """View для отображения списка товаров в корзине пользователя.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для списка товаров.
        model (Model): Модель товара.

    Methods:
        get_queryset: Возвращает товары в корзине текущего пользователя.
        get_context_data: Добавляет текущего пользователя в контекст.
    """

    template_name = "cart-product-list.html"
    context_object_name = "products"
    model = ProductModel

    def get_queryset(self):
        """Возвращает товары в корзине текущего пользователя.

        Returns:
            QuerySet: Список товаров в корзине.
        """
        cart = Cart.objects.get_or_create(user=self.request.user)[0]
        return ProductModel.objects.filter(cart_products__cart=cart)

    def get_context_data(self, **kwargs):
        """Добавляет текущего пользователя в контекст.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        return context


class FavoriteProductListView(LoginRequiredMixin, ListView):
    """View для отображения списка избранных товаров пользователя.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для списка товаров.
        model (Model): Модель товара.

    Methods:
        get_queryset: Возвращает избранные товары текущего пользователя.
        get_context_data: Добавляет текущего пользователя в контекст.
    """

    template_name = "favorite-product-list.html"
    context_object_name = "products"
    model = ProductModel

    def get_queryset(self):
        """Возвращает избранные товары текущего пользователя.

        Returns:
            QuerySet: Список избранных товаров.
        """
        favorite = Favorite.objects.get_or_create(user=self.request.user)[0]
        return ProductModel.objects.filter(favorite_products__favorite=favorite)

    def get_context_data(self, **kwargs):
        """Добавляет текущего пользователя в контекст.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        return context


class CheckoutView(LoginRequiredMixin, FormView):
    """View для оформления заказа.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        form_class (Form): Класс формы оформления заказа.

    Methods:
        get_context_data: Добавляет выбранные товары и общую стоимость в контекст.
        get: Обрабатывает AJAX-запрос для получения выбранных товаров.
        form_valid: Обрабатывает успешное оформление заказа.
    """

    template_name = "checkout.html"
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        """Добавляет выбранные товары и общую стоимость в контекст.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        selected_ids = self.request.session.get("selected_products", [])
        products = ProductModel.objects.filter(id__in=selected_ids)
        context["products"] = products
        context["total_price"] = sum(product.price for product in products)
        return context

    def get(self, request, *args, **kwargs):
        """Обрабатывает AJAX-запрос для получения выбранных товаров.

        Args:
            request: HttpRequest объект.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            JsonResponse: Список товаров и общая стоимость в JSON.
            Или стандартный HttpResponse для обычного GET-запроса.
        """
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            print("Start load")
            selected_ids = json.loads(request.GET.get("selected_products", "[]"))
            request.session["selected_products"] = selected_ids
            products = ProductModel.objects.filter(id__in=selected_ids)
            serializer = ProductSerializer(products, many=True)
            return JsonResponse(
                {
                    "products": serializer.data,
                    "total_price": sum(product.price for product in products),
                }
            )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Обрабатывает успешное оформление заказа.

        Args:
            form: Валидная форма заказа.

        Returns:
            HttpResponse: Результат родительского form_valid.
        """
        selected_ids = self.request.session.get("selected_products", [])
        products = ProductModel.objects.filter(id__in=selected_ids)
        # Здесь логика создания заказа
        return super().form_valid(form)
import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView

from .forms import ProductForm, OrderForm, CheckoutForm
from .filters import ProductFilter
from .models import ProductModel
from profiles_app.models import UserProfileModel
from shop_app_api.models import CartProduct, Cart, FavoriteProduct, Favorite

from shop_app_api.serializers import ProductSerializer


class ShopMainPageView(ListView):
    template_name = 'shop-main.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['my_user'] = user
            context['profile'] = get_object_or_404(UserProfileModel, user=user)

        context['form'] = self.filterset.form
        return context


class ProductDetailView(DetailView):
    template_name = 'product-detail.html'
    context_object_name = 'product'
    model = ProductModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['my_user'] = user
        return context


class ProductListView(ListView):
    template_name = 'product-list.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['my_user'] = user
            context['profile'] = get_object_or_404(UserProfileModel, user=user)

        context['form'] = self.filterset.form
        return context


class MyProductView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'my-product.html'
    context_object_name = 'products'
    model = ProductModel
    form_class = ProductFilter

    def has_permission(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return render(self.request, 'error/product-forbidden.html')

    def get_queryset(self):
        return ProductModel.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_user'] = self.request.user
        context['profile'] = get_object_or_404(UserProfileModel, user=self.request.user)
        context['search_form'] = self.form_class(self.request.GET)
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'product-create.html'
    context_object_name = 'product'
    form_class = ProductForm
    model = ProductModel

    def has_permission(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return render(self.request, 'error/product-forbidden.html')

    def form_valid(self, form):
        product = form.save(user=self.request.user, commit=True)
        product.save()
        return redirect(reverse('shop_app:product_list'))

    def form_invalid(self, form):
        print('Form is invalid:', form.errors)
        return render(self.request, self.template_name, {
            'form': form,
            'product': form.instance
        })


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'product-update.html'
    context_object_name = 'product'
    model = ProductModel
    form_class = ProductForm

    def has_permission(self):
        self.object = self.get_object()
        return self.request.user.is_staff and self.request.user == self.object.created_by

    def handle_no_permission(self):
        return render(self.request, 'error/product-forbidden.html')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        return redirect(reverse('shop_app:product_detail', kwargs={'pk': self.object.pk}))


class ProductDeleteView(DeleteView):
    template_name = 'product-delete.html'
    context_object_name = 'product'
    model = ProductModel


class CartProductListView(LoginRequiredMixin, ListView):
    template_name = 'cart-product-list.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        cart = Cart.objects.get_or_create(user=self.request.user)[0]
        return ProductModel.objects.filter(
            cart_products__cart=cart
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_user'] = self.request.user
        return context


class FavoriteProductListView(LoginRequiredMixin, ListView):
    template_name = 'favorite-product-list.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        favorite = Favorite.objects.get_or_create(user=self.request.user)[0]
        return ProductModel.objects.filter(
            favoriteproduct__favorite=favorite
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_user'] = self.request.userCartProduct
        return context


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_ids = self.request.session.get('selected_products', [])
        products = ProductModel.objects.filter(id__in=selected_ids)
        context['products'] = products
        context['total_price'] = sum(product.price for product in products)
        return context

    def get(self, request, *args, **kwargs):
        # Получаем выбранные товары из sessionStorage (переданные через AJAX)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print("Start load")
            selected_ids = json.loads(request.GET.get('selected_products', '[]'))
            request.session['selected_products'] = selected_ids
            products = ProductModel.objects.filter(id__in=selected_ids)
            serializer = ProductSerializer(products, many=True)
            return JsonResponse({
                'products': serializer.data,
                'total_price': sum(product.price for product in products)
            })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Обработка успешного оформления заказа
        selected_ids = self.request.session.get('selected_products', [])
        products = ProductModel.objects.filter(id__in=selected_ids)
        # Здесь логика создания заказа
        return super().form_valid(form)

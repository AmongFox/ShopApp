from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from .forms import ProductForm
from .filters import ProductFilter
from .models import ProductModel
from profiles_app.models import UserProfileModel


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


class CartProductListView(ListView):
    template_name = 'cart-product-list.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProductModel.objects.filter(cart_product__user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_user'] = self.request.user
        return context


class FavoriteProductListView(ListView):
    template_name = 'favorite-product-list.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProductModel.objects.filter(favorite_product__user=user)

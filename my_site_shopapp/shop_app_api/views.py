from django.db import transaction
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartProduct, FavoriteProduct, OrderItem, Order, Cart, Favorite
from .serializers import (
    CartProductSerializer,
    FavoriteProductSerializer,
    OrderSerializer,
    ProductSerializer,
)
from shop_app.models import ProductModel


class AddToCartAPIView(CreateAPIView):
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_product, created = CartProduct.objects.get_or_create(
            cart=self.get_cart(),
            product=serializer.validated_data["product"],
            defaults={"quantity": serializer.validated_data.get("quantity", 1)},
        )

        if not created:
            cart_product.quantity += serializer.validated_data.get("quantity", 1)
            cart_product.save()

        output_serializer = CartProductSerializer(cart_product)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class RemoveFromCartAPIView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToFavoriteAPIView(CreateAPIView):
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_favorite(self):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        return favorite

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        favorite_product, created = FavoriteProduct.objects.get_or_create(
            favorite=self.get_favorite(),
            product=serializer.validated_data["product"],
        )

        if not created:
            favorite_product.save()

        output_serializer = FavoriteProductSerializer(favorite_product)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class FavoriteProductDeleteView(DestroyAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Валидация базовых данных
        items = request.data.get("items", [])

        if not items:
            return Response(
                {"error": "Заказ должен содержать хотя бы один товар"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создаем заказ
        order = Order.objects.create(user=request.user, status="created")

        total_price = 0
        order_items = []

        # Обрабатываем каждый товар в заказе
        for item in items:
            try:
                product = ProductModel.objects.get(pk=item["product_id"])
                quantity = int(item["quantity"])

                if quantity < 1:
                    order.delete()
                    return Response(
                        {"error": "Количество товара должно быть не менее 1"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                price = product.price * quantity
                total_price += price

                order_items.append(
                    OrderItem(
                        order=order, product=product, quantity=quantity, price=price
                    )
                )

            except (KeyError, ValueError):
                order.delete()
                return Response(
                    {"error": "Неверный формат данных товаров"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except ProductModel.DoesNotExist:
                order.delete()
                return Response(
                    {"error": f'Товар с ID {item["product_id"]} не найден'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Сохраняем все товары заказа
        OrderItem.objects.bulk_create(order_items)

        # Обновляем общую сумму
        order.total_price = total_price
        order.save()

        # Возвращаем созданный заказ
        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class SelectedProductsAPI(APIView):
    def post(self, request):
        try:
            selected_ids = request.data.get("selected_products", [])

            # Проверяем, что товары действительно существуют
            existing_products = ProductModel.objects.filter(id__in=selected_ids)
            existing_ids = [str(product.id) for product in existing_products]

            # Сохраняем только существующие товары
            request.session["selected_products"] = existing_ids

            serializer = ProductSerializer(existing_products, many=True)
            return Response(
                {
                    "products": serializer.data,
                    "total_price": sum(product.price for product in existing_products),
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

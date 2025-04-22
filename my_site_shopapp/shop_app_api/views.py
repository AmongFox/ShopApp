from django.db import transaction
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_app.models import ProductModel

from .models import Cart, CartProduct, Favorite, FavoriteProduct, Order, OrderItem
from .serializers import (
    CartProductSerializer,
    FavoriteProductSerializer,
    OrderSerializer,
    ProductSerializer,
)


class AddToCartAPIView(CreateAPIView):
    """API endpoint для добавления товаров в корзину пользователя.

    Attributes:
        serializer_class (Serializer): Сериализатор для товаров корзины.
        permission_classes (list): Требует аутентификации пользователя.

    Methods:
        get_cart: Получает или создает корзину для текущего пользователя.
        create: Добавляет товар в корзину или увеличивает количество существующего.
    """

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        """Получает корзину текущего пользователя или создает новую.

        Returns:
            Cart: Объект корзины пользователя.
        """
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def create(self, request, *args, **kwargs):
        """Добавляет товар в корзину пользователя.

        Args:
            request (Request): Объект запроса с данными товара.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Сериализованные данные товара в корзине с HTTP_201_CREATED.
        """
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
    """API endpoint для удаления товаров из корзины.

    Attributes:
        queryset (QuerySet): Набор объектов CartProduct.
        serializer_class (Serializer): Сериализатор для товаров корзины.
        permission_classes (list): Требует аутентификации пользователя.

    Methods:
        destroy: Удаляет товар из корзины пользователя.
    """

    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """Удаляет товар из корзины пользователя.

        Args:
            request (Request): Объект запроса.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Пустой ответ с HTTP_204_NO_CONTENT.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToFavoriteAPIView(CreateAPIView):
    """API endpoint для добавления товаров в избранное.

    Attributes:
        serializer_class (Serializer): Сериализатор для избранных товаров.
        permission_classes (list): Требует аутентификации пользователя.

    Methods:
        get_favorite: Получает или создает список избранного для пользователя.
        create: Добавляет товар в избранное пользователя.
    """

    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_favorite(self):
        """Получает список избранного текущего пользователя или создает новый.

        Returns:
            Favorite: Объект избранного пользователя.
        """
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        return favorite

    def create(self, request, *args, **kwargs):
        """Добавляет товар в избранное пользователя.

        Args:
            request (Request): Объект запроса с данными товара.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Сериализованные данные товара в избранном с HTTP_201_CREATED.
        """
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
    """API endpoint для удаления товаров из избранного.

    Attributes:
        queryset (QuerySet): Набор объектов FavoriteProduct.
        serializer_class (Serializer): Сериализатор для избранных товаров.
        permission_classes (list): Требует аутентификации пользователя.

    Methods:
        destroy: Удаляет товар из избранного пользователя.
    """

    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """Удаляет товар из избранного пользователя.

        Args:
            request (Request): Объект запроса.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Пустой ответ с HTTP_204_NO_CONTENT.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCreateView(CreateAPIView):
    """API endpoint для создания заказов.

    Attributes:
        queryset (QuerySet): Набор объектов Order.
        serializer_class (Serializer): Сериализатор для заказов.
        permission_classes (list): Требует аутентификации пользователя.

    Methods:
        create: Создает новый заказ с товарами.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создает новый заказ на основе переданных товаров.

        Args:
            request (Request): Объект запроса с данными заказа.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Сериализованные данные заказа с HTTP_201_CREATED при успехе.
                     Сообщения об ошибках с соответствующими статусами при неудаче.

        Raises:
            KeyError: При отсутствии обязательных полей в данных товара.
            ValueError: При неверном формате данных.
            ProductModel.DoesNotExist: При указании несуществующего товара.
        """
        items = request.data.get("items", [])

        if not items:
            return Response(
                {"error": "Заказ должен содержать хотя бы один товар"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(user=request.user, status="created")

        total_price = 0
        order_items = []

        try:
            with transaction.atomic():
                for item in items:
                    product = ProductModel.objects.get(pk=item["product_id"])
                    quantity = int(item["quantity"])

                    if quantity < 1:
                        raise ValueError("Количество товара должно быть не менее 1")

                    price = product.price * quantity
                    total_price += price

                    order_items.append(
                        OrderItem(
                            order=order, product=product, quantity=quantity, price=price
                        )
                    )

                OrderItem.objects.bulk_create(order_items)
                order.total_price = total_price
                order.save()

        except (KeyError, ValueError) as e:
            order.delete()
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ProductModel.DoesNotExist:
            order.delete()
            return Response(
                {"error": 'Товар с указанным ID не найден'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class SelectedProductsAPI(APIView):
    """API endpoint для работы с выбранными товарами в сессии.

    Methods:
        post: Сохраняет выбранные товары в сессии пользователя.
    """

    def post(self, request):
        """Сохраняет выбранные товары в сессии и возвращает информацию о них.

        Args:
            request (Request): Объект запроса с ID выбранных товаров.

        Returns:
            Response: Данные о выбранных товарах и их общей стоимости.
                     Сообщение об ошибке с HTTP_500_INTERNAL_SERVER_ERROR при неудаче.
        """
        try:
            selected_ids = request.data.get("selected_products", [])

            existing_products = ProductModel.objects.filter(id__in=selected_ids)
            existing_ids = [str(product.id) for product in existing_products]

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
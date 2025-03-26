from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartProduct, FavoriteProduct
from .serializers import CartProductSerializer, FavoriteProductSerializer


class CartProductCreateView(CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        existing_cart = CartProduct.objects.filter(
            user=serializer.validated_data['user'],
            product=serializer.validated_data['product']
        )

        if existing_cart.exists():
            existing_cart.update(quantity=existing_cart.first().quantity + serializer.validated_data['quantity'])
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartProductDeleteView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteProductCreateView(CreateAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        existing_favorite = FavoriteProduct.objects.filter(
            user=serializer.validated_data['user'],
            product=serializer.validated_data['product']
        )

        if existing_favorite.exists():
            return Response({'error': 'Product already added to favorites'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavoriteProductDeleteView(DestroyAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteProductCheckView(APIView):
    def get(self, request, product_id):
        is_favorite = FavoriteProduct.objects.filter(user=request.user, product_id=product_id).exists()
        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)

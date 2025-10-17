from rest_framework import status, viewsets, permissions, mixins
from rest_framework.response import Response
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from favorites.services.product_service import get_product
from favorites.docs import favorite_docs


@favorite_docs
class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            return Favorite.objects.filter(client=user)
        return Favorite.objects.none()

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        product_data = get_product(product_id)

        if not product_data:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(
            data=request.data,
            context={'client': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user, product_snapshot=product_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
